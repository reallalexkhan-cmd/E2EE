"""
╔═══════════════════════════════════════════════════════════════╗
║     DARKSTAR BOII SAHIIL - 24/7 BACKGROUND WORKER             ║
║           NONSTOP AUTOMATION - HEARTBEAT MONITOR               ║
╚═══════════════════════════════════════════════════════════════╝
Developer: Darkstar Boii Sahiil

This worker runs continuously to:
1. Monitor automation health
2. Auto-restart crashed automations
3. Process scheduled messages
4. Clean up old logs
5. Update statistics
"""

import time
import threading
import schedule
import logging
from datetime import datetime, timedelta
import database_enhanced as db
from automation_engine import automation_manager

logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - [WORKER] %(message)s'
)
logger = logging.getLogger(__name__)

class BackgroundWorker:
    """24/7 Background Worker for automation management"""
    
    def __init__(self):
        self.running = False
        self.check_interval = 60  # seconds
        self.heartbeat_timeout = 120  # seconds
        
    def start(self):
        """Start the background worker"""
        self.running = True
        logger.info("🚀 Background Worker started!")
        
        while self.running:
            try:
                self.check_heartbeats()
                self.process_scheduled_messages()
                self.cleanup_old_logs()
                self.update_stats()
            except Exception as e:
                logger.error(f"Worker error: {e}")
            
            time.sleep(self.check_interval)
    
    def stop(self):
        """Stop the background worker"""
        self.running = False
        logger.info("🛑 Background Worker stopped")
    
    def check_heartbeats(self):
        """Check automation heartbeats and restart if needed"""
        active_automations = db.get_active_automations()
        
        for automation in active_automations:
            user_id = automation['user_id']
            last_heartbeat = automation.get('last_heartbeat')
            
            if last_heartbeat:
                # Check if heartbeat is stale
                try:
                    hb_time = datetime.fromisoformat(str(last_heartbeat).replace('Z', '+00:00'))
                    if datetime.now(hb_time.tzinfo) - hb_time > timedelta(seconds=self.heartbeat_timeout):
                        logger.warning(f"⚠️ Stale heartbeat for user {user_id}, checking...")
                        
                        # Check if should auto-restart
                        config = db.get_user_config(user_id)
                        if config and config.get('auto_restart'):
                            logger.info(f"🔄 Auto-restarting automation for user {user_id}")
                            automation_manager.start_automation(user_id, config)
                except Exception as e:
                    logger.error(f"Heartbeat check error: {e}")
    
    def process_scheduled_messages(self):
        """Process scheduled messages that are due"""
        # This would be implemented to check and send scheduled messages
        pass
    
    def cleanup_old_logs(self):
        """Clean up logs older than 7 days"""
        # Implementation for log cleanup
        pass
    
    def update_stats(self):
        """Update daily statistics"""
        # Implementation for stats updates
        pass


# Global worker instance
background_worker = BackgroundWorker()

def start_background_worker():
    """Start the background worker in a separate thread"""
    worker_thread = threading.Thread(target=background_worker.start, daemon=True)
    worker_thread.start()
    return worker_thread


if __name__ == "__main__":
    print("🚀 Starting Darkstar E2EE Background Worker...")
    start_background_worker()
    
    try:
        while True:
            time.sleep(1)
    except KeyboardInterrupt:
        print("\n🛑 Shutting down...")
        background_worker.stop()