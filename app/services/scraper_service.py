"""
Scraper Service with Email Notifications
"""

import os
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from sqlalchemy.orm import Session
from typing import List

from app.models import PriceAlert, Price, Product

class NotificationService:
    def __init__(self):
        self.smtp_server = os.getenv("SMTP_SERVER", "smtp.gmail.com")
        self.smtp_port = int(os.getenv("SMTP_PORT", "587"))
        self.smtp_username = os.getenv("SMTP_USERNAME")
        self.smtp_password = os.getenv("SMTP_PASSWORD")
        self.from_email = os.getenv("FROM_EMAIL", "alerts@priceaggregator.com")

    def send_email(self, to_email: str, subject: str, body: str, html: bool = False):
        """Send email notification"""
        if not self.smtp_username or not self.smtp_password:
            print(f"⚠️ Email not configured. Would send to {to_email}:")
            print(f"Subject: {subject}")
            return False

        try:
            msg = MIMEMultipart()
            msg['From'] = self.from_email
            msg['To'] = to_email
            msg['Subject'] = subject

            content_type = 'html' if html else 'plain'
            msg.attach(MIMEText(body, content_type))

            server = smtplib.SMTP(self.smtp_server, self.smtp_port)
            server.starttls()
            server.login(self.smtp_username, self.smtp_password)
            server.send_message(msg)
            server.quit()

            print(f"✅ Email sent to {to_email}")
            return True
        except Exception as e:
            print(f"❌ Email failed: {e}")
            return False

    def send_alert_notification(self, alert: PriceAlert, price: Price, product: Product):
        """Send price alert notification"""
        if not alert.email:
            return

        subject = f"🚨 Price Alert: {product.name}"

        body = f"""
        <html>
        <body style="font-family: Arial, sans-serif;">
            <h2>Price Alert Triggered!</h2>
            <p><strong>Product:</strong> {product.name}</p>
            <p><strong>Current Price:</strong> ${price.price}</p>
            <p><strong>Your Target:</strong> ${alert.target_price} ({alert.condition})</p>
            <p><a href="{price.listing_url}" style="background: #007bff; color: white; padding: 10px 20px; text-decoration: none; border-radius: 5px;">View Deal</a></p>
        </body>
        </html>
        """

        self.send_email(alert.email, subject, body, html=True)

    def send_webhook(self, url: str, payload: dict):
        """Send webhook notification"""
        import requests
        try:
            response = requests.post(url, json=payload, timeout=10)
            return response.status_code == 200
        except Exception as e:
            print(f"❌ Webhook failed: {e}")
            return False

class ScraperService:
    def __init__(self, db: Session):
        self.db = db
        self.notification = NotificationService()

    def process_scraped_data(self, product_data: dict, prices: List[dict]):
        """Process scraped data and save to database"""
        # Find or create product
        product = self.db.query(Product).filter(
            Product.name == product_data['name'],
            Product.category == product_data['category']
        ).first()

        if not product:
            product = Product(**product_data)
            self.db.add(product)
            self.db.flush()

        # Add prices
        for price_data in prices:
            price = Price(product_id=product.id, **price_data)
            self.db.add(price)

        self.db.commit()

        # Check alerts
        self.check_alerts_for_product(product.id)

        return product

    def check_alerts_for_product(self, product_id: int):
        """Check and trigger alerts for a product"""
        from datetime import datetime

        alerts = self.db.query(PriceAlert).filter(
            PriceAlert.product_id == product_id,
            PriceAlert.is_active == True
        ).all()

        latest_price = self.db.query(Price).filter(
            Price.product_id == product_id
        ).order_by(Price.scraped_at.desc()).first()

        if not latest_price:
            return

        product = self.db.query(Product).filter(Product.id == product_id).first()

        for alert in alerts:
            triggered = False

            if alert.condition == "below" and latest_price.price <= alert.target_price:
                triggered = True
            elif alert.condition == "above" and latest_price.price >= alert.target_price:
                triggered = True

            if triggered:
                alert.last_triggered = datetime.utcnow()
                alert.trigger_count += 1
                self.db.commit()

                # Send notifications
                if alert.email:
                    self.notification.send_alert_notification(alert, latest_price, product)

                if alert.webhook_url:
                    self.notification.send_webhook(alert.webhook_url, {
                        "product_id": product_id,
                        "product_name": product.name,
                        "current_price": latest_price.price,
                        "target_price": alert.target_price,
                        "condition": alert.condition
                    })
