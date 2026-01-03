import time
import csv
import os
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from webdriver_manager.chrome import ChromeDriverManager
from selenium.common.exceptions import TimeoutException, StaleElementReferenceException

#region agent log helper
def _agent_log(hypothesis_id, location, message, data):
    payload = {
        "sessionId": "debug-session",
        "runId": "run1",
        "hypothesisId": hypothesis_id,
        "location": location,
        "message": message,
        "data": data,
        "timestamp": int(time.time() * 1000),
    }
    try:
        log_path = r"c:\Users\User\Desktop\new\.cursor\debug.log"
        os.makedirs(os.path.dirname(log_path), exist_ok=True)
        with open(log_path, "a", encoding="utf-8") as _f:
            _f.write(f"{payload}\\n")
    except Exception:
        pass
#endregion

#region agent log startup
_agent_log("H0", "backend.py:module", "module_loaded", {})
#endregion

#region plan content change wait helper
def wait_for_plan_content_change(driver, initial_content, timeout=30):
    """
    Wait for the plan container content to change from the initial content.
    This confirms that old plans are cleared and new plans are loading/loaded.
    Also waits for content to stabilize (no changes for a short period).
    
    Args:
        driver: Selenium WebDriver instance
        initial_content: The initial HTML/text content of the plan container
        timeout: Maximum time to wait in seconds
    
    Returns:
        bool: True if content changed and stabilized, False if timeout
    """
    try:
        def content_changed(driver):
            try:
                step_one = driver.find_element(By.ID, "step_1")
                current_content = step_one.get_attribute("innerHTML") or step_one.text or ""
                # Content changed if it's different from initial
                return current_content != initial_content
            except (StaleElementReferenceException, Exception):
                # Element might be refreshing, which is a sign of change
                return True
        
        # Wait for content to change
        WebDriverWait(driver, timeout).until(content_changed)
        
        # Wait for content to stabilize (no changes for 1 second)
        stable_count = 0
        last_content = get_plan_container_content(driver)
        for _ in range(10):  # Check 10 times over ~1 second
            time.sleep(0.1)
            current_content = get_plan_container_content(driver)
            if current_content == last_content:
                stable_count += 1
                if stable_count >= 3:  # Stable for 3 checks (~0.3 seconds)
                    return True
            else:
                stable_count = 0
                last_content = current_content
        
        return True  # Content changed, even if not fully stable
    except TimeoutException:
        return False

def get_plan_container_content(driver):
    """
    Get the current content (HTML) of the plan container.
    
    Args:
        driver: Selenium WebDriver instance
    
    Returns:
        str: The HTML content of #step_1 element, or empty string if not found
    """
    try:
        step_one = driver.find_element(By.ID, "step_1")
        return step_one.get_attribute("innerHTML") or step_one.text or ""
    except Exception:
        return ""
#endregion

def automate_dropdowns():
    print("=" * 50)
    print("🌍 DROPDOWN AUTOMATION SCRIPT")
    print("=" * 50)
    
    # Terminal se 2 inputs lena (country and state only)
    country_input = input("\n🌍 Enter the country name (exact as on site): ").strip()
    first_state_input = input("\n📍 Enter the FIRST state name to start with: ").strip()
    website_url = input("\n🌐 Enter the website URL: ").strip()
    
    #region agent log
    _agent_log("H1", "backend.py:automate_dropdowns", "function_entry", {
        "country": country_input, 
        "first_state": first_state_input,
        "url": website_url
    })
    #endregion
    
    if not country_input:
        print("❌ Error: Please enter a valid country name")
        return
    if not first_state_input:
        print("❌ Error: Please enter a valid first state name")
        return
    if not website_url:
        print("❌ Error: Please enter a valid URL")
        return
    
    print(f"\n🔗 Opening: {website_url}")
    
    # Predefined forward options array
    forward_options_array = [
    "Afghanistan", "Aland Islands", "Albania", "Algeria", "American Samoa", "Andorra",
    "Angola", "Anguilla", "Antarctica", "Antigua And Barbuda", "Argentina", "Armenia",
    "Aruba", "Australia", "Austria", "Azerbaijan", "Bahamas", "Bahrain", "Bangladesh",
    "Barbados", "Belarus", "Belgium", "Belize", "Benin", "Bermuda", "Bhutan", "Bolivia",
    "Bonaire, Sint Eustatius And Saba", "Bosnia And Herzegovina", "Botswana",
    "Bouvet Island", "Brazil", "British Indian Ocean Territory", "Brunei Darussalam",
    "Bulgaria", "Burkina Faso", "Burundi", "Cambodia", "Cameroon", "Canada",
    "Cape Verde", "Cayman Islands", "Central African Republic", "Chad", "Chile",
    "China", "Christmas Island", "Cocos (Keeling) Islands", "Colombia", "Comoros",
    "Congo, Republic Of", "Cook Islands", "Costa Rica", "Croatia", "Cuba", "Curacao",
    "Cyprus", "Czech Republic", "Democratic Republic of the Congo", "Denmark",
    "Djibouti", "Dominica", "Dominican Republic", "Ecuador", "Egypt", "El Salvador",
    "Equatorial Guinea", "Eritrea", "Estonia", "Ethiopia", "Falkland Islands",
    "Faroe Islands", "Fiji", "Finland", "France", "French Guiana", "French Polynesia",
    "French Southern Lands", "Gabon", "Gambia", "Georgia", "Germany", "Ghana",
    "Gibraltar", "Greece", "Greenland", "Grenada", "Guadeloupe", "Guam", "Guatemala",
    "Guernsey", "Guinea", "Guinea-Bissau", "Guyana", "Haiti",
    "Heard And Mcdonald Islands", "Honduras", "Hong Kong", "Hungary", "Iceland",
    "India", "Indonesia", "Iran", "Iraq", "Ireland", "Isle Of Man", "Israel", "Italy",
    "Jamaica", "Japan", "Jersey", "Jordan", "Kazakhstan", "Kenya", "Kiribati",
    "Korea, North", "Korea, South", "Kosovo", "Kuwait", "Kyrgyzstan", "Laos",
    "Latvia", "Lebanon", "Lesotho", "Liberia", "Libya", "Liechtenstein",
    "Lithuania", "Luxembourg", "Macau", "Macedonia", "Madagascar", "Malawi",
    "Malaysia", "Maldives", "Mali", "Malta", "Marshall Islands", "Martinique",
    "Mauritania", "Mauritius", "Mayotte", "Mexico", "Micronesia", "Moldova",
    "Monaco", "Mongolia", "Montenegro", "Montserrat", "Morocco", "Mozambique",
    "Myanmar", "Namibia", "Nauru", "Nepal", "Netherlands", "Netherlands Antilles",
    "New Caledonia", "New Zealand", "Nicaragua", "Niger", "Nigeria", "Niue",
    "Norfolk Island", "Northern Mariana Islands", "Norway", "Not Applicable",
    "Oman", "Pakistan", "Palau", "Palestine", "Panama", "Papua New Guinea",
    "Paraguay", "Peru", "Philippines", "Pitcairn", "Poland", "Portugal",
    "Puerto Rico", "Qatar", "Reunion", "Romania", "Russian Federation", "Rwanda",
    "Saint Barthelemy", "Saint Helena, Ascension And Tristan Da Cunha",
    "Saint Kitts And Nevis", "Saint Lucia", "Saint Martin",
    "Saint Pierre And Miquelon", "Saint Vincent And The Grenadines", "Samoa",
    "San Marino", "Sao Tome And Principe", "Satellite", "Saudi Arabia", "Senegal",
    "Serbia", "Seychelles", "Sierra Leone", "Singapore",
    "Sint Maarten (Dutch Part)", "Slovakia", "Slovenia", "Solomon Islands",
    "Somalia", "South Africa", "South Georgia And South Sandwich Islands",
    "South Sudan", "Spain", "Sri Lanka", "Sudan", "Suriname",
    "Svalbard And Jan Mayen Islands", "Swaziland", "Sweden", "Switzerland",
    "Syria", "Taiwan", "Tajikistan", "Tanzania", "Thailand", "Timor-Leste",
    "Togo", "Tokelau", "Tonga", "Trinidad And Tobago", "Tunisia", "Turkey",
    "Turkmenistan", "Turks And Caicos Islands", "Tuvalu", "Uganda", "Ukraine",
    "United Arab Emirates", "United Kingdom",
    "United States Minor Outlying Islands", "United States of America",
    "Uruguay", "Uzbekistan", "Vanuatu", "Vatican City", "Venezuela", "Vietnam",
    "Virgin Islands, British", "Virgin Islands, U.S.", "VoIP/SIP",
    "Wallis And Futuna Islands", "Western Sahara", "Yemen", "Zambia", "Zimbabwe"
    ]

    
    print(f"\n📋 Using predefined forward options array with {len(forward_options_array)} countries")
    
    # Global driver variable
    global driver
    
    try:
        # Chrome options
        chrome_options = Options()
        chrome_options.add_argument("--start-maximized")
        chrome_options.add_argument("--disable-notifications")
        chrome_options.add_experimental_option("excludeSwitches", ["enable-logging"])
        
        # Initialize driver
        print("🚀 Initializing browser...")
        driver = webdriver.Chrome(
            service=Service(ChromeDriverManager().install()),
            options=chrome_options
        )
        
        # Navigate to website
        print("📡 Navigating to website...")
        driver.get(website_url)
        time.sleep(3)
        
        # Wait for page to load
        print("⏳ Waiting for page to load...")
        WebDriverWait(driver, 20).until(
            EC.presence_of_element_located((By.XPATH, "//h4[contains(text(), 'SELECT A PHONE NUMBER')]"))
        )
        print("✅ Page loaded successfully")
        
        # ========== STEP 1: COUNTRY DROPDOWN ==========
        print("\n1️⃣ Selecting Country...")
        
        # Country dropdown click
        try:
            country_dropdown = WebDriverWait(driver, 10).until(
                EC.element_to_be_clickable((By.ID, "originatingCountrySelect"))
            )
            country_dropdown.click()
            print("   ✓ Clicked country dropdown")
        except:
            # Alternative locator
            country_dropdown = WebDriverWait(driver, 10).until(
                EC.element_to_be_clickable((By.CSS_SELECTOR, "div[name='country']"))
            )
            country_dropdown.click()
            print("   ✓ Clicked country dropdown (using name)")
        
        time.sleep(1)
        
        # Type user-provided country in search
        print(f"   🔍 Searching for '{country_input}'...")
        search_input = WebDriverWait(driver, 10).until(
            EC.element_to_be_clickable((By.CSS_SELECTOR, "#originatingCountrySelect input[type='search']"))
        )
        search_input.clear()
        search_input.send_keys(country_input)
        # Wait for search results to appear
        WebDriverWait(driver, 5).until(
            EC.presence_of_element_located((By.CSS_SELECTOR, "div.ant-select-dropdown:not(.ant-select-dropdown-hidden) div.ant-select-item-option"))
        )
        
        # Select country
        try:
            country_option = WebDriverWait(driver, 5).until(
                EC.element_to_be_clickable((By.XPATH, f"//div[contains(@class, 'ant-select-item') and contains(., '{country_input}')]"))
            )
            country_option.click()
            print(f"   ✅ Selected country: {country_input}")
        except:
            search_input.send_keys(Keys.ENTER)
            print(f"   ✅ Selected country: {country_input} (using Enter)")
        
        # Capture selected country text
        selected_country = country_input
        try:
            selected_country = driver.find_element(By.CSS_SELECTOR, "#originatingCountrySelect .ant-select-selection-item").text.strip() or selected_country
        except:
            pass
        
        # Wait for plan content to change after country selection
        print("   ⏳ Waiting for plan content to update after country selection...")
        initial_plan_content = get_plan_container_content(driver)
        if wait_for_plan_content_change(driver, initial_plan_content, timeout=30):
            print("   ✅ Plan content updated")
        else:
            print("   ⚠️ Plan content change timeout, proceeding anyway...")
        
        # ========== STEP 2: FIRST STATE SELECTION ==========
        print("\n2️⃣ Selecting First State...")
        
        def open_state_dropdown():
            try:
                element = WebDriverWait(driver, 10).until(
                    EC.element_to_be_clickable((By.ID, "numberTypeSelect"))
                )
                element.click()
                return element
            except:
                element = WebDriverWait(driver, 10).until(
                    EC.element_to_be_clickable((By.CSS_SELECTOR, "div[name='numberType']"))
                )
                element.click()
                return element
        
        # Open state dropdown
        open_state_dropdown()
        # Wait for dropdown options to be visible
        WebDriverWait(driver, 5).until(
            EC.presence_of_element_located((By.CSS_SELECTOR, "div.ant-select-dropdown:not(.ant-select-dropdown-hidden) div.ant-select-item-option"))
        )
        
        # Type first state in search
        print(f"   🔍 Searching for '{first_state_input}'...")
        state_search_input = WebDriverWait(driver, 10).until(
            EC.element_to_be_clickable((By.CSS_SELECTOR, "#numberTypeSelect input[type='search']"))
        )
        state_search_input.clear()
        state_search_input.send_keys(first_state_input)
        # Wait for search results to appear
        WebDriverWait(driver, 5).until(
            EC.presence_of_element_located((By.CSS_SELECTOR, "div.ant-select-dropdown:not(.ant-select-dropdown-hidden) div.ant-select-item-option"))
        )
        
        # Select first state
        try:
            state_option = WebDriverWait(driver, 5).until(
                EC.element_to_be_clickable((By.XPATH, f"//div[contains(@class, 'ant-select-item') and contains(., '{first_state_input}')]"))
            )
            state_option.click()
            print(f"   ✅ Selected first state: {first_state_input}")
        except:
            state_search_input.send_keys(Keys.ENTER)
            print(f"   ✅ Selected first state: {first_state_input} (using Enter)")
        
        # Capture selected state text from dropdown (single source of truth)
        first_selected_state = None
        try:
            first_selected_state = driver.find_element(By.CSS_SELECTOR, "#numberTypeSelect .ant-select-selection-item").text.strip() or None
        except:
            try:
                first_selected_state = driver.find_element(By.CSS_SELECTOR, "div[name='numberType'] .ant-select-selection-item").text.strip() or None
            except:
                pass
        if not first_selected_state:
            raise ValueError(f"State '{first_state_input}' could not be selected from dropdown")
        
        # Wait for plan content to change after first state selection
        print("   ⏳ Waiting for plan content to update after state selection...")
        initial_plan_content = get_plan_container_content(driver)
        if wait_for_plan_content_change(driver, initial_plan_content, timeout=30):
            print("   ✅ Plan content updated")
        else:
            print("   ⚠️ Plan content change timeout, proceeding anyway...")
        
        # ========== STEP 3: COLLECT ALL STATES WITH SCROLLING ==========
        print("\n3️⃣ Collecting ALL State Options (with scrolling)...")
        
        def collect_all_state_options():
            """Collect all state options with automatic scrolling"""
            all_options = []
            last_count = 0
            
            # Open dropdown
            open_state_dropdown()
            time.sleep(1.5)
            
            # Get dropdown container
            try:
                dropdown_container = driver.find_element(By.CSS_SELECTOR, "div.ant-select-dropdown:not(.ant-select-dropdown-hidden) .rc-virtual-list-holder")
            except:
                dropdown_container = None
            
            # Scroll to collect all options
            max_scroll_attempts = 100
            scroll_attempt = 0
            
            while scroll_attempt < max_scroll_attempts:
                # Get current visible options
                option_elements = driver.find_elements(By.CSS_SELECTOR, "div.ant-select-dropdown:not(.ant-select-dropdown-hidden) div.ant-select-item-option")
                
                for element in option_elements:
                    try:
                        text = element.text.strip()
                        if text and text not in all_options:
                            all_options.append(text)
                    except:
                        continue
                
                # Check if we got new options
                if len(all_options) > last_count:
                    last_count = len(all_options)
                    # Scroll down if we have container
                    if dropdown_container:
                        driver.execute_script("arguments[0].scrollTop += 300;", dropdown_container)
                    else:
                        # Fallback: send down arrow key
                        active_elem = driver.switch_to.active_element
                        active_elem.send_keys(Keys.ARROW_DOWN)
                    time.sleep(0.5)
                else:
                    # Try scrolling a bit more
                    if dropdown_container:
                        driver.execute_script("arguments[0].scrollTop += 100;", dropdown_container)
                    time.sleep(0.3)
                    
                    # Check again
                    option_elements = driver.find_elements(By.CSS_SELECTOR, "div.ant-select-dropdown:not(.ant-select-dropdown-hidden) div.ant-select-item-option")
                    new_options_count = 0
                    for element in option_elements:
                        try:
                            text = element.text.strip()
                            if text and text not in all_options:
                                all_options.append(text)
                                new_options_count += 1
                        except:
                            continue
                    
                    if new_options_count == 0:
                        break
                
                scroll_attempt += 1
            
            # Close dropdown
            try:
                driver.switch_to.active_element.send_keys(Keys.ESCAPE)
            except:
                pass
            
            time.sleep(0.5)
            return all_options
        
        # Collect all states
        state_options = collect_all_state_options()
        print(f"   📊 Found {len(state_options)} total state options")
        
        # Show all states found
        print("\n   📋 All states found:")
        for i, state in enumerate(state_options, 1):
            print(f"      {i:3d}. {state}")
        
        # Find exact dropdown state matching terminal input (case-insensitive)
        matched_state = next((s for s in state_options if s.lower() == first_selected_state.lower()), None)
        if not matched_state:
            raise ValueError(f"Selected state '{first_selected_state}' not found in dropdown options")
        first_selected_state = matched_state
        state_index = state_options.index(matched_state)
        print(f"\n   📍 First state '{first_selected_state}' found at position {state_index + 1}")
        
        # Get states starting from the first selected state (inclusive)
        state_options_to_process = state_options[state_index:]
        print(f"   🔄 Will process {len(state_options_to_process)} states starting from '{first_selected_state}'")
        #region agent log
        _agent_log("H2", "backend.py:state_collection", "collected_states", {
            "total_states": len(state_options), 
            "first_state": first_selected_state,
            "states_to_process": len(state_options_to_process),
            "all_states": state_options
        })
        #endregion
        
        # Helper: select state deterministically via search + verification
        def select_state(state_text):
            open_state_dropdown()
            try:
                search = WebDriverWait(driver, 10).until(
                    EC.element_to_be_clickable((By.CSS_SELECTOR, "#numberTypeSelect input[type='search']"))
                )
                search.clear()
                search.send_keys(state_text)
                WebDriverWait(driver, 5).until(
                    EC.presence_of_element_located((By.CSS_SELECTOR, "div.ant-select-dropdown:not(.ant-select-dropdown-hidden) div.ant-select-item-option"))
                )
                try:
                    option = WebDriverWait(driver, 5).until(
                        EC.element_to_be_clickable((By.XPATH, f"//div[contains(@class,'ant-select-item-option') and normalize-space()='{state_text}']"))
                    )
                    option.click()
                except:
                    search.send_keys(Keys.ENTER)
            except:
                try:
                    driver.switch_to.active_element.send_keys(Keys.ENTER)
                except:
                    pass
            
            # Verify selection and retry once if mismatch
            try:
                selected_label = driver.find_element(By.CSS_SELECTOR, "#numberTypeSelect .ant-select-selection-item").text.strip()
            except:
                selected_label = ""
            if selected_label and selected_label.lower() != state_text.lower():
                open_state_dropdown()
                try:
                    search = WebDriverWait(driver, 10).until(
                        EC.element_to_be_clickable((By.CSS_SELECTOR, "#numberTypeSelect input[type='search']"))
                    )
                    search.clear()
                    search.send_keys(state_text)
                    search.send_keys(Keys.ENTER)
                except:
                    pass

        # ========== STEP 4: PREPARE CSV ==========
        print("\n4️⃣ Starting CSV processing...")
        with open("result.csv", "w", newline="", encoding="utf-8") as csvfile:
            writer = csv.DictWriter(csvfile, fieldnames=["Country", "State", "Forward Calls To", "Plan", "Call Insights", "Call Recording"])
            writer.writeheader()
            
            # ========== STEP 5: PROCESS EACH STATE ==========
            for idx, state_text in enumerate(state_options_to_process, 1):
                current_state_idx = state_index + idx
                print(f"\n{'='*60}")
                print(f"📍 Processing state {idx}/{len(state_options_to_process)}: {state_text}")
                print(f"{'='*60}")
                #region agent log
                _agent_log("H3", "backend.py:state_processing", "processing_state", {
                    "state": state_text, 
                    "index": idx, 
                    "total": len(state_options_to_process),
                    "global_index": current_state_idx
                })
                #endregion
                
                # Select this state (if not the first one already selected)
                if idx > 1 or state_text != first_selected_state:
                    select_state(state_text)
                    print(f"   ✅ Selected state: {state_text}")
                
                # Capture selected state
                selected_state = state_text
                try:
                    selected_state = driver.find_element(By.CSS_SELECTOR, "#numberTypeSelect .ant-select-selection-item").text.strip() or selected_state
                except:
                    pass
                
                # Wait for plan content to change after state selection
                print("   ⏳ Waiting for plan content to update after state selection...")
                initial_plan_content = get_plan_container_content(driver)
                if wait_for_plan_content_change(driver, initial_plan_content, timeout=30):
                    print("   ✅ Plan content updated")
                else:
                    print("   ⚠️ Plan content change timeout, proceeding anyway...")
                
                # ========== STEP 6: FORWARD DROPDOWN HANDLING ==========
                print(f"   📞 Setting up Forward Calls To dropdown for '{selected_state}'...")
                
                def open_forward_dropdown():
                    try:
                        el = WebDriverWait(driver, 10).until(
                            EC.element_to_be_clickable((By.ID, "terminatingCountrySelect"))
                        )
                        el.click()
                        return el
                    except:
                        el = WebDriverWait(driver, 10).until(
                            EC.element_to_be_clickable((By.CSS_SELECTOR, "div[name='userCountry']"))
                        )
                        el.click()
                        return el
                
                # Use predefined forward options array
                print(f"   📊 Using predefined array with {len(forward_options_array)} forward options")
                
                # Show array contents (first 5 only)
                print("   📋 First 5 forward options from array:")
                for i in range(min(5, len(forward_options_array))):
                    print(f"      {i+1}. {forward_options_array[i]}")
                
                # ========== STEP 7: PROCESS EACH FORWARD OPTION ==========
                for fwd_idx, forward_text in enumerate(forward_options_array, 1):
                    forward_label = forward_text
                    print(f"\n   📞 Forward option {fwd_idx}/{len(forward_options_array)}: {forward_text}")
                    #region agent log
                    _agent_log("H5", "backend.py:forward_processing", "processing_forward", {
                        "state": selected_state,
                        "forward": forward_text,
                        "index": fwd_idx,
                        "total": len(forward_options_array)
                    })
                    #endregion
                    
                    # Capture initial plan content before selecting forward option
                    initial_plan_content = get_plan_container_content(driver)
                    
                    # Select this forward option
                    open_forward_dropdown()
                    
                    # Search for forward option (no scrolling needed)
                    try:
                        forward_search = WebDriverWait(driver, 10).until(
                            EC.element_to_be_clickable((By.CSS_SELECTOR, "#terminatingCountrySelect input[type='search']"))
                        )
                        forward_search.clear()
                        forward_search.send_keys(forward_text)
                        
                        # Wait for search results to appear
                        WebDriverWait(driver, 5).until(
                            EC.presence_of_element_located((By.CSS_SELECTOR, "div.ant-select-dropdown:not(.ant-select-dropdown-hidden) div.ant-select-item-option"))
                        )
                        
                        # Try to find and click
                        try:
                            target_fwd = WebDriverWait(driver, 5).until(
                                EC.element_to_be_clickable((By.XPATH, f"//div[contains(@class,'ant-select-item-option') and normalize-space()='{forward_text}']"))
                            )
                            target_fwd.click()
                            print("      ✅ Forward option selected")
                        except:
                            # If not found via click, use Enter
                            forward_search.send_keys(Keys.ENTER)
                            print("      ✅ Forward option selected (via Enter)")
                    except Exception as e:
                        print(f"      ❌ Error selecting forward option: {str(e)}")
                        # Close dropdown and continue
                        try:
                            driver.switch_to.active_element.send_keys(Keys.ESCAPE)
                        except:
                            pass
                        continue
                    
                    # Capture actual selected forward label from UI (source of truth)
                    selected_forward = forward_text
                    try:
                        selected_forward = driver.find_element(By.CSS_SELECTOR, "#terminatingCountrySelect .ant-select-selection-item").text.strip() or selected_forward
                    except:
                        pass
                    # If mismatch, retry selection once to align UI with intended forward_text
                    if selected_forward.lower() != forward_text.lower():
                        try:
                            open_forward_dropdown()
                            forward_search = WebDriverWait(driver, 10).until(
                                EC.element_to_be_clickable((By.CSS_SELECTOR, "#terminatingCountrySelect input[type='search']"))
                            )
                            forward_search.clear()
                            forward_search.send_keys(forward_text)
                            forward_search.send_keys(Keys.ENTER)
                            selected_forward = driver.find_element(By.CSS_SELECTOR, "#terminatingCountrySelect .ant-select-selection-item").text.strip() or selected_forward
                        except:
                            pass
                    
                    # Wait for plan content to change after forward option selection
                    print("      ⏳ Waiting for plan content to update after forward selection...")
                    if wait_for_plan_content_change(driver, initial_plan_content, timeout=30):
                        print("      ✅ Plan content updated")
                    else:
                        print("      ⚠️ Plan content change timeout, proceeding anyway...")
                    
                    # Now scroll and read plan cards
                    print("      📋 Reading plan cards...")
                    plans = []
                    deadline = time.time() + 30
                    
                    while time.time() < deadline and not plans:
                        # Check explicit "No Plans Available" message and bail early
                        try:
                            no_plans_elems = driver.find_elements(By.XPATH, "//*[contains(text(),'No Plans Available')]")
                            if any(elem.is_displayed() for elem in no_plans_elems):
                                print("      ⚠️ No plans available message detected; leaving plan blank")
                                plans = []
                                break
                        except:
                            pass
                        
                        try:
                            # Scroll to plan section
                            step_one = driver.find_element(By.ID, "step_1")
                            driver.execute_script("arguments[0].scrollIntoView({behavior: 'smooth', block: 'center'});", step_one)
                        except:
                            driver.execute_script("window.scrollBy(0, 600);")
                        
                        # Small wait for scroll to complete
                        time.sleep(0.5)
                        
                        # Look for plan cards
                        plan_cards = driver.find_elements(By.XPATH, "//div[starts-with(@id,'business') and contains(@id,'Card')]")
                        if not plan_cards:
                            plan_cards = driver.find_elements(By.XPATH, "//div[contains(@id,'business') and contains(@class,'Card')]")
                        
                        if plan_cards:
                            for card in plan_cards:
                                try:
                                    title_elem = card.find_element(By.XPATH, "./preceding-sibling::div[1]//div[contains(@id,'Title')]")
                                    title = title_elem.text.strip()
                                except:
                                    title = "N/A"
                                try:
                                    text = card.text.strip()
                                except:
                                    text = ""
                                
                                if text:
                                    lines = [title] + [ln.strip() for ln in text.splitlines() if ln.strip()]
                                    merged = "-".join(lines)
                                    if not merged.endswith("."):
                                        merged = merged + "."
                                    plans.append(merged)
                        else:
                            time.sleep(0.5)
                    
                    if not plans:
                        print("      ❌ No plans found")
                        numbered_plan = ""
                    else:
                        print(f"      ✅ Found {len(plans)} plan(s)")
                        numbered_plan = "\n\n".join([f"{p_idx+1}){p}" for p_idx, p in enumerate(plans)])
                    
                    #region agent log
                    _agent_log("H6", "backend.py:plan_collection", "collected_plans", {
                        "state": selected_state,
                        "forward": selected_forward,
                        "plans_found": len(plans)
                    })
                    #endregion
                    
                    # ========== STEP 8: WRITE TO CSV ==========
                    call_insights = (
                        "60-Day Free Trial\n\n"
                        "$10.00/month after Good call quality is key to the smooth operation of your business.\n\n"
                        "With Call Insights, you can monitor key quality metrics such as Mean Opinion Score (MOS),\n\n"
                        "Jitter, and Packet Loss. Stay on top of any standout metrics and proactively troubleshoot with the\n\n"
                        "help of AVOXI's readily available support team; all at the click of a button!\n\n"
                        "Starting monthly plan includes monitoring for 1,000 completed calls with $0.0100 per additional call.\n\n"
                        "Have a high call volume? Upgrade your Call Insights Subscription plan within your AVOXI Portal!\n\n"
                        "Learn more about Call Insights here."
                    )
                    call_recording = (
                        "30-Day Free Trial\n\n"
                        "$6.99/month after Activate call recording on your AVOXI number to record inbound,\n\n"
                        "outbound, or directional calls. Set up the number of days you want to store the call recordings,\n\n"
                        "and you are done. Storage for call recording is FREE. You can play or download the stored call\n\n"
                        "recording at any time."
                    )
                    
                    writer.writerow({
                        "Country": selected_country,
                        "State": selected_state,
                        "Forward Calls To": selected_forward,
                        "Plan": numbered_plan,
                        "Call Insights": call_insights,
                        "Call Recording": call_recording
                    })
                    #region agent log
                    _agent_log("H7", "backend.py:csv_write", "wrote_row", {
                        "country": selected_country,
                        "state": selected_state,
                        "forward": selected_forward,
                        "plans_found": len(plans)
                    })
                    #endregion
                    
                    # Scroll back to forward dropdown
                    try:
                        driver.execute_script("arguments[0].scrollIntoView({behavior: 'smooth', block: 'center'});", driver.find_element(By.ID, "terminatingCountrySelect"))
                    except:
                        driver.execute_script("window.scrollTo(0, 0);")
                
                print(f"   ✅ Completed all forward options for '{selected_state}'")
                
                # Scroll back to state dropdown for next iteration
                try:
                    driver.execute_script("arguments[0].scrollIntoView({behavior: 'smooth', block: 'center'});", driver.find_element(By.ID, "numberTypeSelect"))
                except:
                    driver.execute_script("window.scrollTo(0, 0);")
        
        print("\n" + "=" * 60)
        print("🎉 AUTOMATION COMPLETED SUCCESSFULLY!")
        print("=" * 60)
        print(f"\n📊 Summary:")
        print(f"   • Country: {selected_country} ✓")
        print(f"   • First state: {first_selected_state} ✓")
        print(f"   • Total states processed: {len(state_options_to_process)} ✓")
        print(f"   • Total forward options processed: {len(forward_options_array)} per state ✓")
        print(f"   • Data saved to: result.csv ✓")
        
        # Close browser
        print("\n🔄 Closing browser...")
        time.sleep(2)
        driver.quit()
        print("✅ Browser closed")
        
    except Exception as e:
        print(f"\n❌ ERROR: {str(e)}")
        import traceback
        traceback.print_exc()
        
        print("\n🔧 Possible issues:")
        print("   1. Check website URL")
        print("   2. Check internet connection")
        print("   3. Website structure might have changed")
        print("   4. Check if dropdowns are visible and clickable")
        
        # Try to close browser
        try:
            driver.quit()
        except:
            pass

if __name__ == "__main__":
    automate_dropdowns()
    print("\n✨ Script execution finished!")