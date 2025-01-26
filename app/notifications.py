class NotificationHandler:
    @staticmethod
    def notify(total_products: int, updated_products: int):
        """
        Simple notification strategy - currently just prints to console
        
        Can be easily extended to support:
        - Email notifications
        - Slack/Discord messages
        - SMS alerts
        """
        print(f"Scraping Completed:")
        print(f"Total Products Scraped: {total_products}")
        print(f"Products Updated: {updated_products}")