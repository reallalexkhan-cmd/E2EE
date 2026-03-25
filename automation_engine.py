"""
╔═══════════════════════════════════════════════════════════════╗
║     DARKSTAR BOII SAHIIL - 24/7 AUTOMATION ENGINE v2.0        ║
║           NONSTOP POWER - AUTO-RESTART - HEARTBEAT            ║
╚═══════════════════════════════════════════════════════════════╝
Developer: Darkstar Boii Sahiil
"""

import time
import threading
import random
import logging
import traceback
from datetime import datetime
from pathlib import Path
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException, NoSuchElementException, WebDriverException

import database_enhanced as db

# Setup logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - [%(levelname)s] %(message)s',
    handlers=[
        logging.StreamHandler(),
        logging.FileHandler('automation.log')
    ]
)
logger = logging.getLogger(__name__)

class AutomationEngine:
    """24/7 Nonstop Automation Engine with Auto-Recovery"""
    
    def __init__(self, user_id, config):
        self.user_id = user_id
        self.config = config
        self.process_id = f"AUTO-{user_id}-{int(time.time())}"
        self.driver = None
        self.running = False
        self.paused = False
        self.message_count = 0
        self.error_count = 0
        self.max_errors = 5
        self.message_rotation_index = 0
        self.start_time = None
        self.last_heartbeat = None
        self.heartbeat_interval = 30  # seconds
        
    def log(self, message, level='info'):
        """Add log message"""
        timestamp = datetime.now().strftime("%H:%M:%S")
        formatted_msg = f"[{timestamp}] [{self.process_id}] {message}"
        
        if level == 'error':
            logger.error(formatted_msg)
        elif level == 'warning':
            logger.warning(formatted_msg)
        else:
            logger.info(formatted_msg)
        
        db.add_log(self.user_id, message, level, self.process_id)
    
    def setup_browser(self):
        """Setup Chrome browser with enhanced options"""
        self.log('🚀 Setting up Chrome browser...')
        
        chrome_options = Options()
        chrome_options.add_argument('--headless=new')
        chrome_options.add_argument('--no-sandbox')
        chrome_options.add_argument('--disable-setuid-sandbox')
        chrome_options.add_argument('--disable-dev-shm-usage')
        chrome_options.add_argument('--disable-gpu')
        chrome_options.add_argument('--disable-extensions')
        chrome_options.add_argument('--disable-infobars')
        chrome_options.add_argument('--disable-notifications')
        chrome_options.add_argument('--window-size=1920,1080')
        chrome_options.add_argument('--start-maximized')
        chrome_options.add_argument('--user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/121.0.0.0 Safari/537.36')
        
        # Performance optimizations
        chrome_options.add_argument('--disable-background-networking')
        chrome_options.add_argument('--disable-breakpad')
        chrome_options.add_argument('--disable-component-update')
        chrome_options.add_argument('--disable-default-apps')
        chrome_options.add_argument('--disable-sync')
        chrome_options.add_argument('--metrics-recording-only')
        chrome_options.add_argument('--no-first-run')
        chrome_options.add_argument('--disable-blink-features=AutomationControlled')
        chrome_options.add_experimental_option('excludeSwitches', ['enable-automation'])
        chrome_options.add_experimental_option('useAutomationExtension', False)
        
        chromium_paths = [
            '/usr/bin/chromium',
            '/usr/bin/chromium-browser',
            '/usr/bin/google-chrome',
            '/usr/bin/chrome'
        ]
        
        for chromium_path in chromium_paths:
            if Path(chromium_path).exists():
                chrome_options.binary_location = chromium_path
                self.log(f'✅ Found Chromium at: {chromium_path}')
                break
        
        chromedriver_paths = [
            '/usr/bin/chromedriver',
            '/usr/local/bin/chromedriver'
        ]
        
        driver_path = None
        for driver_candidate in chromedriver_paths:
            if Path(driver_candidate).exists():
                driver_path = driver_candidate
                self.log(f'✅ Found ChromeDriver at: {driver_path}')
                break
        
        try:
            from selenium.webdriver.chrome.service import Service
            
            if driver_path:
                service = Service(executable_path=driver_path)
                self.driver = webdriver.Chrome(service=service, options=chrome_options)
            else:
                self.driver = webdriver.Chrome(options=chrome_options)
            
            self.driver.set_window_size(1920, 1080)
            self.driver.set_page_load_timeout(60)
            self.log('✅ Chrome browser setup completed!')
            return True
            
        except Exception as error:
            self.log(f'❌ Browser setup failed: {error}', 'error')
            return False
    
    def add_cookies(self):
        """Add Facebook cookies"""
        if not self.config.get('cookies') or not self.config['cookies'].strip():
            return False
        
        self.log('🍪 Adding cookies...')
        cookie_array = self.config['cookies'].split(';')
        added_count = 0
        
        for cookie in cookie_array:
            cookie_trimmed = cookie.strip()
            if cookie_trimmed:
                first_equal_index = cookie_trimmed.find('=')
                if first_equal_index > 0:
                    name = cookie_trimmed[:first_equal_index].strip()
                    value = cookie_trimmed[first_equal_index + 1:].strip()
                    try:
                        self.driver.add_cookie({
                            'name': name,
                            'value': value,
                            'domain': '.facebook.com',
                            'path': '/'
                        })
                        added_count += 1
                    except Exception:
                        pass
        
        self.log(f'✅ Added {added_count} cookies')
        return added_count > 0
    
    def find_message_input(self):
        """Find message input with multiple strategies"""
        self.log('🔍 Finding message input...')
        
        # Wait for page to load
        time.sleep(5)
        
        # Try scrolling to trigger lazy loading
        try:
            self.driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
            time.sleep(1)
            self.driver.execute_script("window.scrollTo(0, 0);")
            time.sleep(1)
        except:
            pass
        
        # Primary selectors for Facebook Messenger
        selectors = [
            'div[contenteditable="true"][role="textbox"]',
            'div[contenteditable="true"][data-lexical-editor="true"]',
            'div[aria-label*="message" i][contenteditable="true"]',
            'div[aria-label*="Message" i][contenteditable="true"]',
            'div[contenteditable="true"][spellcheck="true"]',
            '[role="textbox"][contenteditable="true"]',
            'div[data-lexical-editor="true"]',
            '[contenteditable="true"]'
        ]
        
        for idx, selector in enumerate(selectors):
            try:
                elements = self.driver.find_elements(By.CSS_SELECTOR, selector)
                self.log(f'  Selector {idx+1}/{len(selectors)}: Found {len(elements)} elements')
                
                for element in elements:
                    try:
                        # Check if element is visible and editable
                        if element.is_displayed() and element.is_enabled():
                            # Try to focus
                            try:
                                element.click()
                                time.sleep(0.3)
                            except:
                                pass
                            
                            return element
                    except:
                        continue
            except:
                continue
        
        # Fallback: Use JavaScript to find contenteditable
        try:
            element = self.driver.execute_script('''
                const elements = document.querySelectorAll('[contenteditable="true"]');
                for (let el of elements) {
                    if (el.offsetParent !== null) {
                        return el;
                    }
                }
                return null;
            ''')
            if element:
                self.log('✅ Found input via JavaScript')
                return element
        except:
            pass
        
        self.log('❌ Message input not found!', 'error')
        return None
    
    def find_send_button(self):
        """Find send button"""
        selectors = [
            '[aria-label="Press Enter to send"]',
            '[aria-label*="Send"]',
            '[data-testid="send-button"]',
            'div[role="button"][aria-label*="send" i]'
        ]
        
        for selector in selectors:
            try:
                elements = self.driver.find_elements(By.CSS_SELECTOR, selector)
                for element in elements:
                    if element.is_displayed():
                        return element
            except:
                continue
        return None
    
    def send_message(self, message_input, message):
        """Send message using multiple methods"""
        try:
            # Method 1: JavaScript injection
            self.driver.execute_script('''
                const element = arguments[0];
                const message = arguments[1];
                
                element.scrollIntoView({behavior: 'smooth', block: 'center'});
                element.focus();
                element.click();
                
                if (element.tagName === 'DIV') {
                    element.textContent = message;
                    element.innerHTML = message;
                    
                    // Dispatch input events
                    element.dispatchEvent(new Event('input', { bubbles: true }));
                    element.dispatchEvent(new Event('change', { bubbles: true }));
                    element.dispatchEvent(new InputEvent('input', { bubbles: true, data: message }));
                }
            ''', message_input, message)
            
            time.sleep(1)
            
            # Try to find and click send button
            send_btn = self.find_send_button()
            if send_btn:
                try:
                    send_btn.click()
                    self.log(f'✅ Sent via button: "{message[:40]}..."')
                    return True
                except:
                    pass
            
            # Method 2: Press Enter
            self.driver.execute_script('''
                const element = arguments[0];
                element.focus();
                
                const events = [
                    new KeyboardEvent('keydown', { key: 'Enter', code: 'Enter', keyCode: 13, which: 13, bubbles: true }),
                    new KeyboardEvent('keypress', { key: 'Enter', code: 'Enter', keyCode: 13, which: 13, bubbles: true }),
                    new KeyboardEvent('keyup', { key: 'Enter', code: 'Enter', keyCode: 13, which: 13, bubbles: true })
                ];
                
                events.forEach(event => element.dispatchEvent(event));
            ''', message_input)
            
            self.log(f'✅ Sent via Enter: "{message[:40]}..."')
            return True
            
        except Exception as e:
            self.log(f'❌ Send error: {str(e)[:100]}', 'error')
            return False
    
    def get_next_message(self):
        """Get next message from rotation"""
        messages_list = [msg.strip() for msg in self.config.get('messages', '').split('\n') if msg.strip()]
        
        if not messages_list:
            messages_list = ['Hello! 👋', 'Hi there!', 'Hey! How are you?']
        
        message = messages_list[self.message_rotation_index % len(messages_list)]
        self.message_rotation_index += 1
        
        # Add prefix if configured
        if self.config.get('name_prefix'):
            message = f"{self.config['name_prefix']} {message}"
        
        return message
    
    def update_heartbeat(self):
        """Update heartbeat for monitoring"""
        db.update_heartbeat(self.user_id, self.process_id, self.message_count)
        self.last_heartbeat = time.time()
    
    def run(self):
        """Main automation loop with 24/7 capabilities"""
        self.running = True
        self.start_time = time.time()
        self.message_count = 0
        self.error_count = 0
        
        db.set_automation_running(self.user_id, True, self.process_id)
        self.log(f'🚀 Automation started!')
        
        while self.running:
            try:
                # Setup browser
                if not self.setup_browser():
                    self.log('❌ Failed to setup browser, retrying in 30s...', 'error')
                    time.sleep(30)
                    continue
                
                # Navigate to Facebook
                self.log('🌐 Navigating to Facebook...')
                self.driver.get('https://www.facebook.com/')
                time.sleep(5)
                
                # Add cookies
                self.add_cookies()
                
                # Navigate to chat
                chat_id = self.config.get('chat_id', '').strip()
                if chat_id:
                    # Try E2EE URL first
                    e2ee_url = f'https://www.facebook.com/messages/e2ee/t/{chat_id}'
                    normal_url = f'https://www.facebook.com/messages/t/{chat_id}'
                    
                    self.log(f'📱 Opening conversation: {chat_id}')
                    self.driver.get(e2ee_url)
                    time.sleep(5)
                    
                    # Check if we need to fallback to normal URL
                    if '/messages/e2ee' not in self.driver.current_url:
                        self.driver.get(normal_url)
                        time.sleep(5)
                else:
                    self.log('📱 Opening messages...')
                    self.driver.get('https://www.facebook.com/messages')
                    time.sleep(5)
                
                # Find message input
                message_input = self.find_message_input()
                if not message_input:
                    self.log('❌ Message input not found! Refreshing...', 'error')
                    self.driver.refresh()
                    time.sleep(10)
                    message_input = self.find_message_input()
                    
                    if not message_input:
                        self.error_count += 1
                        if self.error_count >= self.max_errors:
                            self.log('❌ Max errors reached, restarting browser...', 'error')
                            self.close_browser()
                            time.sleep(30)
                            continue
                
                # Message sending loop
                delay = int(self.config.get('delay', 30))
                max_messages = int(self.config.get('max_messages', 0))
                
                while self.running and message_input:
                    # Check if paused
                    while self.paused and self.running:
                        time.sleep(1)
                    
                    if not self.running:
                        break
                    
                    # Check max messages
                    if max_messages > 0 and self.message_count >= max_messages:
                        self.log(f'✅ Reached max messages ({max_messages}), stopping...')
                        self.running = False
                        break
                    
                    # Get and send message
                    message = self.get_next_message()
                    
                    if self.send_message(message_input, message):
                        self.message_count += 1
                        self.log(f'📊 Total messages sent: {self.message_count}')
                        
                        # Update heartbeat
                        if time.time() - (self.last_heartbeat or 0) > self.heartbeat_interval:
                            self.update_heartbeat()
                    else:
                        self.error_count += 1
                        if self.error_count >= self.max_errors:
                            break
                    
                    # Wait for delay
                    self.log(f'⏳ Waiting {delay} seconds...')
                    for _ in range(delay):
                        if not self.running:
                            break
                        time.sleep(1)
                
                # Check if should auto-restart
                if self.config.get('auto_restart', 1) and not self.running:
                    self.log('🔄 Auto-restarting automation...')
                    self.close_browser()
                    time.sleep(10)
                    self.running = True
                    continue
                
            except WebDriverException as e:
                self.log(f'❌ WebDriver error: {str(e)[:200]}', 'error')
                self.error_count += 1
                
            except Exception as e:
                self.log(f'❌ Fatal error: {str(e)[:200]}', 'error')
                self.log(traceback.format_exc()[:500], 'error')
                self.error_count += 1
            
            finally:
                self.close_browser()
        
        # Cleanup
        self.log('🛑 Automation stopped')
        db.set_automation_running(self.user_id, False)
        db.update_stats(self.user_id, self.message_count, int(time.time() - (self.start_time or time.time())))
    
    def close_browser(self):
        """Close browser safely"""
        if self.driver:
            try:
                self.driver.quit()
                self.log('✅ Browser closed')
            except:
                pass
            self.driver = None
    
    def stop(self):
        """Stop automation"""
        self.running = False
        self.log('🛑 Stop signal received')
    
    def pause(self):
        """Pause automation"""
        self.paused = True
        self.log('⏸️ Automation paused')
    
    def resume(self):
        """Resume automation"""
        self.paused = False
        self.log('▶️ Automation resumed')


class AutomationManager:
    """Manager for multiple automation instances"""
    
    def __init__(self):
        self.instances = {}
        self.lock = threading.Lock()
    
    def start_automation(self, user_id, config):
        """Start automation for a user"""
        with self.lock:
            if user_id in self.instances and self.instances[user_id].running:
                return False, "Automation already running"
            
            engine = AutomationEngine(user_id, config)
            thread = threading.Thread(target=engine.run, daemon=True)
            thread.start()
            
            self.instances[user_id] = engine
            return True, f"Automation started with process ID: {engine.process_id}"
    
    def stop_automation(self, user_id):
        """Stop automation for a user"""
        with self.lock:
            if user_id in self.instances:
                self.instances[user_id].stop()
                del self.instances[user_id]
                return True, "Automation stopped"
            return False, "No automation running"
    
    def get_status(self, user_id):
        """Get automation status"""
        with self.lock:
            if user_id in self.instances:
                engine = self.instances[user_id]
                return {
                    'running': engine.running,
                    'paused': engine.paused,
                    'message_count': engine.message_count,
                    'process_id': engine.process_id,
                    'uptime': time.time() - (engine.start_time or time.time())
                }
            return {'running': False}
    
    def pause_automation(self, user_id):
        """Pause automation"""
        with self.lock:
            if user_id in self.instances:
                self.instances[user_id].pause()
                return True
            return False
    
    def resume_automation(self, user_id):
        """Resume automation"""
        with self.lock:
            if user_id in self.instances:
                self.instances[user_id].resume()
                return True
            return False


# Global automation manager instance
automation_manager = AutomationManager()