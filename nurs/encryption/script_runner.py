from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from pathlib import Path

class Encryption:
    def __init__(self):
        self.chrome_options = self._configure_chrome_options()
        self.current_dir = Path(__file__).parent
        self.encrypt_file = self.current_dir / 'encrypt.js'

    @staticmethod
    def _configure_chrome_options():
        """Configure Chrome options for headless execution"""
        options = Options()
        options.add_argument('--headless')
        options.add_argument('--no-sandbox')
        options.add_argument('--disable-dev-shm-usage')
        return options

    def _create_temp_html(self):
        """Create temporary HTML file with encryption script"""
        html_content = f"""
        <!DOCTYPE html>
        <html>
            <head>
                <script src="file://{self.encrypt_file}"></script>
            </head>
            <body></body>
        </html>
        """
        temp_html_path = self.current_dir / 'temp.html'
        with open(temp_html_path, 'w') as f:
            f.write(html_content)
        return temp_html_path

    def _execute_script(self, script):
        """Execute JavaScript encryption function"""
        driver = webdriver.Chrome(options=self.chrome_options)
        temp_html_path = self._create_temp_html()
        try:
            driver.get(f'file://{temp_html_path}')
            encrypted_data = driver.execute_script(script)
            
            return encrypted_data

        except Exception as e:
            print(f"Error running encryption script: {str(e)}")
            return None

        finally:
            driver.quit()
            if temp_html_path.exists():
                temp_html_path.unlink()

    def get_provider(self, nilam_data) -> str:
        """Encrypt nilam data"""
        return self._execute_script(f'return encrypt_nilam({nilam_data})')

    def get_bearer_authorization(self, token) -> str:
        """Get bearer authorization token"""
        return self._execute_script(f'return get_bearer("{token}")')