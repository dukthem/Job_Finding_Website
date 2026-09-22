from typing import List, Dict, Optional

# ====================================================================
# 1. Direct ATS Search URL Patterns for Major ATS Providers
# ====================================================================
ATS_SEARCH_PATTERNS: Dict[str, str] = {
    "greenhouse": "https://boards.greenhouse.io/{slug}?query={role}",
    "lever": "https://jobs.lever.co/{slug}?query={role}",
    "workday": "https://{slug}.wd3.myworkdayjobs.com/en-US/Careers?q={role}",
    "smartrecruiters": "https://jobs.smartrecruiters.com/{slug}?q={role}",
    "direct": "{url}"
}

# Specific deep-search queries for Big Tech, Unicorns & Global IT Services
COMPANY_JOB_SEARCH_PATTERNS: Dict[str, str] = {
    "google": "https://www.google.com/about/careers/applications/jobs/results/?q={role}",
    "microsoft": "https://jobs.careers.microsoft.com/global/en/search?q={role}",
    "amazon": "https://www.amazon.jobs/en/search?base_query={role}",
    "apple": "https://jobs.apple.com/en-in/search?search={role}",
    "meta": "https://www.metacareers.com/jobs?q={role}",
    "netflix": "https://jobs.netflix.com/search?q={role}",
    "nvidia": "https://nvidia.wd5.myworkdayjobs.com/NVIDIAExternalCareerSite?q={role}",
    "adobe": "https://careers.adobe.com/us/en/search-results?keywords={role}",
    "salesforce": "https://salesforce.wd12.myworkdayjobs.com/External_Career_Site?q={role}",
    "stripe": "https://boards.greenhouse.io/stripe?query={role}",
    "spotify": "https://jobs.lever.co/spotify?query={role}",
    "uber": "https://www.uber.com/global/en/careers/list/?query={role}",
    "razorpay": "https://boards.greenhouse.io/razorpay?query={role}",
    "tcs": "https://www.tcs.com/careers/india?q={role}",
    "infosys": "https://career.infosys.com/joblist?keyword={role}",
    "wipro": "https://careers.wipro.com/careers-home/jobs?keywords={role}",
    "cognizant": "https://careers.cognizant.com/global-en/jobs/?keyword={role}",
    "accenture": "https://www.accenture.com/in-en/careers/jobsearch?jk={role}",
    "capgemini": "https://www.capgemini.com/in-en/careers/job-search/?search={role}"
}

# ====================================================================
# 2. Curated Directory of Top 200 Tech Companies Worldwide
# ====================================================================
TOP_200_COMPANIES: List[Dict] = [
    # 1. Big Tech & Global Hardware/Software Giants (25)
    {"name": "Google", "category": "Big Tech", "career_url": "https://careers.google.com", "ats_slug": "google"},
    {"name": "Microsoft", "category": "Big Tech", "career_url": "https://jobs.careers.microsoft.com", "ats_slug": "microsoft"},
    {"name": "Amazon", "category": "Big Tech", "career_url": "https://amazon.jobs", "ats_slug": "amazon"},
    {"name": "Apple", "category": "Big Tech", "career_url": "https://jobs.apple.com", "ats_slug": "apple"},
    {"name": "Meta", "category": "Big Tech", "career_url": "https://metacareers.com", "ats_slug": "meta"},
    {"name": "Netflix", "category": "Big Tech", "career_url": "https://jobs.netflix.com", "ats_slug": "netflix"},
    {"name": "NVIDIA", "category": "Big Tech", "career_url": "https://nvidia.wd5.myworkdayjobs.com/NVIDIAExternalCareerSite", "ats_slug": "nvidia"},
    {"name": "Adobe", "category": "Big Tech", "career_url": "https://careers.adobe.com", "ats_slug": "adobe"},
    {"name": "Salesforce", "category": "Big Tech", "career_url": "https://salesforce.wd12.myworkdayjobs.com/External_Career_Site", "ats_slug": "salesforce"},
    {"name": "Oracle", "category": "Big Tech", "career_url": "https://oracle.com/careers", "ats_slug": "oracle"},
    {"name": "Intel", "category": "Big Tech", "career_url": "https://jobs.intel.com", "ats_slug": "intel"},
    {"name": "AMD", "category": "Big Tech", "career_url": "https://careers.amd.com", "ats_slug": "amd"},
    {"name": "Cisco", "category": "Big Tech", "career_url": "https://jobs.cisco.com", "ats_slug": "cisco"},
    {"name": "IBM", "category": "Big Tech", "career_url": "https://ibm.com/careers", "ats_slug": "ibm"},
    {"name": "Qualcomm", "category": "Big Tech", "career_url": "https://qualcomm.wd5.myworkdayjobs.com/External", "ats_slug": "qualcomm"},
    {"name": "Broadcom", "category": "Semiconductor", "career_url": "https://broadcom.com/careers", "ats_slug": "broadcom"},
    {"name": "Texas Instruments", "category": "Semiconductor", "career_url": "https://careers.ti.com", "ats_slug": "ti"},
    {"name": "Sony", "category": "Consumer Tech", "career_url": "https://sony.com/careers", "ats_slug": "sony"},
    {"name": "Samsung", "category": "Hardware / Mobile", "career_url": "https://samsung.com/careers", "ats_slug": "samsung"},
    {"name": "Dell Technologies", "category": "Hardware / Cloud", "career_url": "https://jobs.dell.com", "ats_slug": "dell"},
    {"name": "HP", "category": "Hardware / Software", "career_url": "https://jobs.hp.com", "ats_slug": "hp"},
    {"name": "VMware", "category": "Cloud / Virtualization", "career_url": "https://careers.vmware.com", "ats_slug": "vmware"},
    {"name": "SAP", "category": "Enterprise Software", "career_url": "https://jobs.sap.com", "ats_slug": "sap"},
    {"name": "ServiceNow", "category": "Cloud / Workflow", "career_url": "https://servicenow.com/careers", "ats_slug": "servicenow"},
    {"name": "Workday", "category": "Enterprise Cloud", "career_url": "https://workday.com/careers", "ats_slug": "workday"},

    # 2. Global Product SaaS, Cloud & Developer Tools (40)
    {"name": "Stripe", "category": "Fintech", "career_url": "https://stripe.com/jobs", "ats_slug": "stripe"},
    {"name": "Databricks", "category": "Data / AI", "career_url": "https://databricks.com/company/careers", "ats_slug": "databricks"},
    {"name": "Snowflake", "category": "Data / Cloud", "career_url": "https://snowflake.com/careers", "ats_slug": "snowflake"},
    {"name": "OpenAI", "category": "AI Research", "career_url": "https://openai.com/careers", "ats_slug": "openai"},
    {"name": "Anthropic", "category": "AI Research", "career_url": "https://anthropic.com/careers", "ats_slug": "anthropic"},
    {"name": "GitHub", "category": "Developer Tools", "career_url": "https://github.com/about/careers", "ats_slug": "github"},
    {"name": "GitLab", "category": "Developer Tools", "career_url": "https://about.gitlab.com/jobs", "ats_slug": "gitlab"},
    {"name": "Atlassian", "category": "Product SaaS", "career_url": "https://atlassian.com/company/careers", "ats_slug": "atlassian"},
    {"name": "Cloudflare", "category": "Cloud / Security", "career_url": "https://cloudflare.com/careers", "ats_slug": "cloudflare"},
    {"name": "Figma", "category": "Design Tech", "career_url": "https://figma.com/careers", "ats_slug": "figma"},
    {"name": "Notion", "category": "Productivity", "career_url": "https://notion.so/careers", "ats_slug": "notion"},
    {"name": "Canva", "category": "Design Tech", "career_url": "https://lifeatcanva.com", "ats_slug": "canva"},
    {"name": "Slack", "category": "Productivity", "career_url": "https://slack.com/careers", "ats_slug": "slack"},
    {"name": "Zoom", "category": "Collaboration", "career_url": "https://careers.zoom.us", "ats_slug": "zoom"},
    {"name": "Twilio", "category": "Cloud / API", "career_url": "https://twilio.com/company/jobs", "ats_slug": "twilio"},
    {"name": "Palantir", "category": "Data / AI", "career_url": "https://palantir.com/careers", "ats_slug": "palantir"},
    {"name": "DoorDash", "category": "Consumer Tech", "career_url": "https://careers.doordash.com", "ats_slug": "doordash"},
    {"name": "Pinterest", "category": "Consumer Tech", "career_url": "https://pinterestcareers.com", "ats_slug": "pinterest"},
    {"name": "Dropbox", "category": "Cloud Storage", "career_url": "https://dropbox.com/jobs", "ats_slug": "dropbox"},
    {"name": "Square", "category": "Fintech", "career_url": "https://block.xyz/careers", "ats_slug": "square"},
    {"name": "Shopify", "category": "E-Commerce", "career_url": "https://shopify.com/careers", "ats_slug": "shopify"},
    {"name": "HubSpot", "category": "Marketing SaaS", "career_url": "https://hubspot.com/careers", "ats_slug": "hubspot"},
    {"name": "MongoDB", "category": "Databases", "career_url": "https://mongodb.com/careers", "ats_slug": "mongodb"},
    {"name": "Supabase", "category": "Developer Tools", "career_url": "https://supabase.com/careers", "ats_slug": "supabase"},
    {"name": "Elastic", "category": "Search / Data", "career_url": "https://elastic.co/about/careers", "ats_slug": "elastic"},
    {"name": "Linear", "category": "Developer Tools", "career_url": "https://linear.app/careers", "ats_slug": "linear"},
    {"name": "Airtable", "category": "Productivity", "career_url": "https://airtable.com/careers", "ats_slug": "airtable"},
    {"name": "Miro", "category": "Visual Collaboration", "career_url": "https://miro.com/careers", "ats_slug": "miro"},
    {"name": "Webflow", "category": "Web Tech", "career_url": "https://webflow.com/careers", "ats_slug": "webflow"},
    {"name": "Vercel", "category": "Frontend Cloud", "career_url": "https://vercel.com/careers", "ats_slug": "vercel"},
    {"name": "Datadog", "category": "Observability / Cloud", "career_url": "https://datadoghq.com/careers", "ats_slug": "datadog"},
    {"name": "Splunk", "category": "Data / Security", "career_url": "https://splunk.com/careers", "ats_slug": "splunk"},
    {"name": "CrowdStrike", "category": "Cybersecurity", "career_url": "https://crowdstrike.com/careers", "ats_slug": "crowdstrike"},
    {"name": "HashiCorp", "category": "DevOps / Cloud", "career_url": "https://hashicorp.com/careers", "ats_slug": "hashicorp"},
    {"name": "PagerDuty", "category": "DevOps / Operations", "career_url": "https://pagerduty.com/careers", "ats_slug": "pagerduty"},
    {"name": "Asana", "category": "Project Management", "career_url": "https://asana.com/jobs", "ats_slug": "asana"},
    {"name": "Box", "category": "Cloud Content", "career_url": "https://box.com/careers", "ats_slug": "box"},
    {"name": "Okta", "category": "Identity / Security", "career_url": "https://okta.com/careers", "ats_slug": "okta"},
    {"name": "New Relic", "category": "Observability", "career_url": "https://newrelic.com/about/careers", "ats_slug": "newrelic"},
    {"name": "Grammarly", "category": "AI / Productivity", "career_url": "https://grammarly.com/jobs", "ats_slug": "grammarly"},

    # 3. Global Fintech & Neobanks (25)
    {"name": "Revolut", "category": "Fintech", "career_url": "https://revolut.com/careers", "ats_slug": "revolut"},
    {"name": "Klarna", "category": "Fintech", "career_url": "https://klarna.com/careers", "ats_slug": "klarna"},
    {"name": "Adyen", "category": "Fintech", "career_url": "https://careers.adyen.com", "ats_slug": "adyen"},
    {"name": "Wise", "category": "Fintech", "career_url": "https://wise.jobs", "ats_slug": "wise"},
    {"name": "N26", "category": "Fintech", "career_url": "https://n26.com/careers", "ats_slug": "n26"},
    {"name": "Monzo", "category": "Fintech", "career_url": "https://monzo.com/careers", "ats_slug": "monzo"},
    {"name": "Checkout.com", "category": "Fintech", "career_url": "https://checkout.com/careers", "ats_slug": "checkout"},
    {"name": "Robinhood", "category": "Fintech", "career_url": "https://robinhood.com/careers", "ats_slug": "robinhood"},
    {"name": "Coinbase", "category": "Crypto / Web3", "career_url": "https://coinbase.com/careers", "ats_slug": "coinbase"},
    {"name": "Chime", "category": "Fintech", "career_url": "https://chime.com/careers", "ats_slug": "chime"},
    {"name": "Affirm", "category": "Fintech", "career_url": "https://affirm.com/careers", "ats_slug": "affirm"},
    {"name": "Plaid", "category": "Fintech API", "career_url": "https://plaid.com/careers", "ats_slug": "plaid"},
    {"name": "Brex", "category": "Fintech", "career_url": "https://brex.com/careers", "ats_slug": "brex"},
    {"name": "Ramp", "category": "Fintech", "career_url": "https://ramp.com/careers", "ats_slug": "ramp"},
    {"name": "SoFi", "category": "Fintech", "career_url": "https://sofi.com/careers", "ats_slug": "sofi"},
    {"name": "Ripple", "category": "Crypto / Web3", "career_url": "https://ripple.com/careers", "ats_slug": "ripple"},
    {"name": "Toast", "category": "Fintech / SaaS", "career_url": "https://pos.toasttab.com/careers", "ats_slug": "toast"},
    {"name": "Bill.com", "category": "Fintech", "career_url": "https://bill.com/careers", "ats_slug": "bill"},
    {"name": "Marqeta", "category": "Fintech", "career_url": "https://marqeta.com/company/careers", "ats_slug": "marqeta"},
    {"name": "Remitly", "category": "Fintech", "career_url": "https://remitly.com/careers", "ats_slug": "remitly"},
    {"name": "PayPal", "category": "Payments", "career_url": "https://careers.pypl.com", "ats_slug": "paypal"},
    {"name": "Visa", "category": "Payments", "career_url": "https://visa.com/careers", "ats_slug": "visa"},
    {"name": "Mastercard", "category": "Payments", "career_url": "https://mastercard.com/careers", "ats_slug": "mastercard"},
    {"name": "Bloomberg", "category": "Financial Tech", "career_url": "https://bloomberg.com/careers", "ats_slug": "bloomberg"},
    {"name": "Citadel Securities", "category": "Quantitative Tech", "career_url": "https://citadelsecurities.com/careers", "ats_slug": "citadel"},

    # 4. European Tech Leaders & AI Labs (30)
    {"name": "Spotify", "category": "Consumer Tech", "career_url": "https://lifeatspotify.com", "ats_slug": "spotify"},
    {"name": "DeepMind", "category": "AI Research", "career_url": "https://deepmind.google/about/careers", "ats_slug": "deepmind"},
    {"name": "Mistral AI", "category": "AI Research", "career_url": "https://mistral.ai/careers", "ats_slug": "mistral"},
    {"name": "ASML", "category": "Semiconductor", "career_url": "https://asml.com/careers", "ats_slug": "asml"},
    {"name": "Delivery Hero", "category": "Consumer Tech", "career_url": "https://deliveryhero.com/careers", "ats_slug": "deliveryhero"},
    {"name": "Supercell", "category": "Gaming Tech", "career_url": "https://supercell.com/careers", "ats_slug": "supercell"},
    {"name": "Bolt", "category": "Mobility", "career_url": "https://bolt.eu/careers", "ats_slug": "bolt"},
    {"name": "Personio", "category": "HR Tech", "career_url": "https://personio.com/about-personio/careers", "ats_slug": "personio"},
    {"name": "Celonis", "category": "Enterprise AI", "career_url": "https://celonis.com/careers", "ats_slug": "celonis"},
    {"name": "King", "category": "Gaming Tech", "career_url": "https://king.com/jobs", "ats_slug": "king"},
    {"name": "Rovio", "category": "Gaming Tech", "career_url": "https://rovio.com/careers", "ats_slug": "rovio"},
    {"name": "Skyscanner", "category": "Travel Tech", "career_url": "https://skyscanner.net/jobs", "ats_slug": "skyscanner"},
    {"name": "BlaBlaCar", "category": "Mobility", "career_url": "https://blablacar.com/careers", "ats_slug": "blablacar"},
    {"name": "Kry", "category": "HealthTech", "career_url": "https://kry.health/careers", "ats_slug": "kry"},
    {"name": "Wolt", "category": "Consumer Tech", "career_url": "https://wolt.com/careers", "ats_slug": "wolt"},
    {"name": "Northvolt", "category": "CleanTech", "career_url": "https://northvolt.com/careers", "ats_slug": "northvolt"},
    {"name": "BioNTech", "category": "BioTech", "career_url": "https://biontech.com/careers", "ats_slug": "biontech"},
    {"name": "Arm", "category": "Semiconductor", "career_url": "https://arm.com/careers", "ats_slug": "arm"},
    {"name": "Siemens", "category": "Industrial Tech", "career_url": "https://siemens.com/careers", "ats_slug": "siemens"},
    {"name": "Bosch", "category": "Engineering / IoT", "career_url": "https://bosch.com/careers", "ats_slug": "bosch"},
    {"name": "Zalando", "category": "E-Commerce", "career_url": "https://jobs.zalando.com", "ats_slug": "zalando"},
    {"name": "Just Eat Takeaway", "category": "Food Delivery", "career_url": "https://careers.justeattakeaway.com", "ats_slug": "justeat"},
    {"name": "HelloFresh", "category": "FoodTech", "career_url": "https://hellofresh.com/careers", "ats_slug": "hellofresh"},
    {"name": "Booking.com", "category": "Travel Tech", "career_url": "https://booking.com/careers", "ats_slug": "booking"},
    {"name": "Trustpilot", "category": "Consumer Reviews", "career_url": "https://trustpilot.com/jobs", "ats_slug": "trustpilot"},
    {"name": "Babbel", "category": "EdTech", "career_url": "https://babbel.com/careers", "ats_slug": "babbel"},
    {"name": "SoundCloud", "category": "Audio Tech", "career_url": "https://soundcloud.com/jobs", "ats_slug": "soundcloud"},
    {"name": "Deezer", "category": "Audio Tech", "career_url": "https://deezer.com/careers", "ats_slug": "deezer"},
    {"name": "Infobip", "category": "Communications", "career_url": "https://infobip.com/careers", "ats_slug": "infobip"},
    {"name": "Bitpanda", "category": "Crypto Fintech", "career_url": "https://bitpanda.com/careers", "ats_slug": "bitpanda"},

    # 5. Top Indian Product Unicorns & Startups (45)
    {"name": "Razorpay", "category": "Fintech", "career_url": "https://razorpay.com/jobs", "ats_slug": "razorpay"},
    {"name": "CRED", "category": "Fintech", "career_url": "https://cred.club/careers", "ats_slug": "cred"},
    {"name": "Zomato", "category": "Consumer Tech", "career_url": "https://zomato.com/careers", "ats_slug": "zomato"},
    {"name": "Swiggy", "category": "Consumer Tech", "career_url": "https://swiggy.com/careers", "ats_slug": "swiggy"},
    {"name": "Zerodha", "category": "Fintech", "career_url": "https://zerodha.com/careers", "ats_slug": "zerodha"},
    {"name": "Flipkart", "category": "E-Commerce", "career_url": "https://flipkartcareers.com", "ats_slug": "flipkart"},
    {"name": "PhonePe", "category": "Fintech", "career_url": "https://phonepe.com/careers", "ats_slug": "phonepe"},
    {"name": "Paytm", "category": "Fintech", "career_url": "https://paytm.com/careers", "ats_slug": "paytm"},
    {"name": "Meesho", "category": "E-Commerce", "career_url": "https://meesho.io/careers", "ats_slug": "meesho"},
    {"name": "Groww", "category": "Fintech", "career_url": "https://groww.in/careers", "ats_slug": "groww"},
    {"name": "Urban Company", "category": "Consumer Tech", "career_url": "https://urbancompany.com/careers", "ats_slug": "urbancompany"},
    {"name": "InMobi", "category": "AdTech", "career_url": "https://inmobi.com/company/careers", "ats_slug": "inmobi"},
    {"name": "Postman", "category": "Developer Tools", "career_url": "https://postman.com/careers", "ats_slug": "postman"},
    {"name": "BrowserStack", "category": "Developer Tools", "career_url": "https://browserstack.com/careers", "ats_slug": "browserstack"},
    {"name": "Freshworks", "category": "SaaS", "career_url": "https://freshworks.com/company/careers", "ats_slug": "freshworks"},
    {"name": "Zoho", "category": "SaaS", "career_url": "https://zoho.com/careers", "ats_slug": "zoho"},
    {"name": "Pine Labs", "category": "Fintech", "career_url": "https://pinelabs.com/careers", "ats_slug": "pinelabs"},
    {"name": "Delhivery", "category": "Logistics Tech", "career_url": "https://delhivery.com/careers", "ats_slug": "delhivery"},
    {"name": "Nykaa", "category": "E-Commerce", "career_url": "https://nykaa.com/careers", "ats_slug": "nykaa"},
    {"name": "Zepto", "category": "Quick Commerce", "career_url": "https://zeptonow.com/careers", "ats_slug": "zepto"},
    {"name": "Blinkit", "category": "Quick Commerce", "career_url": "https://blinkit.com/careers", "ats_slug": "blinkit"},
    {"name": "Dream11", "category": "Gaming Tech", "career_url": "https://dreamsports.group/careers", "ats_slug": "dream11"},
    {"name": "PolicyBazaar", "category": "InsurTech", "career_url": "https://policybazaar.com/careers", "ats_slug": "policybazaar"},
    {"name": "Ola", "category": "Mobility", "career_url": "https://olaelectric.com/careers", "ats_slug": "ola"},
    {"name": "CoinSwitch", "category": "Crypto / Web3", "career_url": "https://coinswitch.co/careers", "ats_slug": "coinswitch"},
    {"name": "Cars24", "category": "AutoTech", "career_url": "https://cars24.com/careers", "ats_slug": "cars24"},
    {"name": "Lenskart", "category": "D2C Tech", "career_url": "https://lenskart.com/careers", "ats_slug": "lenskart"},
    {"name": "ShareChat", "category": "Social Media", "career_url": "https://sharechat.com/careers", "ats_slug": "sharechat"},
    {"name": "Upstox", "category": "Fintech", "career_url": "https://upstox.com/careers", "ats_slug": "upstox"},
    {"name": "Khatabook", "category": "Fintech", "career_url": "https://khatabook.com/careers", "ats_slug": "khatabook"},
    {"name": "Classplus", "category": "EdTech", "career_url": "https://classplus.co/careers", "ats_slug": "classplus"},
    {"name": "Apna", "category": "Jobs Tech", "career_url": "https://apna.co/careers", "ats_slug": "apna"},
    {"name": "Spinny", "category": "AutoTech", "career_url": "https://spinny.com/careers", "ats_slug": "spinny"},
    {"name": "Rebel Foods", "category": "FoodTech", "career_url": "https://rebelfoods.com/careers", "ats_slug": "rebelfoods"},
    {"name": "Purplle", "category": "E-Commerce", "career_url": "https://purplle.com/careers", "ats_slug": "purplle"},
    {"name": "Mamaearth", "category": "D2C Tech", "career_url": "https://honasa.in/careers", "ats_slug": "mamaearth"},
    {"name": "Games24x7", "category": "Gaming Tech", "career_url": "https://games24x7.com/careers", "ats_slug": "games24x7"},
    {"name": "Navi", "category": "Fintech", "career_url": "https://navi.com/careers", "ats_slug": "navi"},
    {"name": "CoinDCX", "category": "Crypto / Web3", "career_url": "https://coindcx.com/careers", "ats_slug": "coindcx"},
    {"name": "PhysicsWallah", "category": "EdTech", "career_url": "https://pw.live/careers", "ats_slug": "pw"},
    {"name": "Unacademy", "category": "EdTech", "career_url": "https://unacademy.com/careers", "ats_slug": "unacademy"},
    {"name": "LeadSquared", "category": "SaaS CRM", "career_url": "https://leadsquared.com/careers", "ats_slug": "leadsquared"},
    {"name": "Darwinbox", "category": "HR Tech SaaS", "career_url": "https://darwinbox.com/careers", "ats_slug": "darwinbox"},
    {"name": "CleverTap", "category": "Retention Cloud", "career_url": "https://clevertap.com/careers", "ats_slug": "clevertap"},
    {"name": "Rapido", "category": "Mobility", "career_url": "https://rapido.bike/careers", "ats_slug": "rapido"},

    # 6. Major IT, Cloud & Digital Engineering Services (35)
    {"name": "TCS", "category": "IT Services", "career_url": "https://tcs.com/careers", "ats_slug": "tcs"},
    {"name": "Infosys", "category": "IT Services", "career_url": "https://career.infosys.com", "ats_slug": "infosys"},
    {"name": "Wipro", "category": "IT Services", "career_url": "https://careers.wipro.com", "ats_slug": "wipro"},
    {"name": "HCLTech", "category": "IT Services", "career_url": "https://hcltech.com/careers", "ats_slug": "hcltech"},
    {"name": "Cognizant", "category": "IT Services", "career_url": "https://careers.cognizant.com", "ats_slug": "cognizant"},
    {"name": "Tech Mahindra", "category": "IT Services", "career_url": "https://techmahindra.com/careers", "ats_slug": "techmahindra"},
    {"name": "LTIMindtree", "category": "IT Services", "career_url": "https://ltimindtree.com/careers", "ats_slug": "ltimindtree"},
    {"name": "Accenture", "category": "IT Services", "career_url": "https://accenture.com/careers", "ats_slug": "accenture"},
    {"name": "Capgemini", "category": "IT Services", "career_url": "https://capgemini.com/careers", "ats_slug": "capgemini"},
    {"name": "Persistent Systems", "category": "IT Services", "career_url": "https://persistent.com/careers", "ats_slug": "persistent"},
    {"name": "Mphasis", "category": "IT Services", "career_url": "https://mphasis.com/careers", "ats_slug": "mphasis"},
    {"name": "Coforge", "category": "IT Services", "career_url": "https://coforge.com/careers", "ats_slug": "coforge"},
    {"name": "Birlasoft", "category": "IT Services", "career_url": "https://birlasoft.com/careers", "ats_slug": "birlasoft"},
    {"name": "Hexaware", "category": "IT Services", "career_url": "https://hexaware.com/careers", "ats_slug": "hexaware"},
    {"name": "Tata Elxsi", "category": "Design & Tech", "career_url": "https://tataelxsi.com/careers", "ats_slug": "tataelxsi"},
    {"name": "KPIT", "category": "Automotive Tech", "career_url": "https://kpit.com/careers", "ats_slug": "kpit"},
    {"name": "Cyient", "category": "Engineering Services", "career_url": "https://cyient.com/careers", "ats_slug": "cyient"},
    {"name": "Genpact", "category": "Tech & Ops", "career_url": "https://genpact.com/careers", "ats_slug": "genpact"},
    {"name": "DXC Technology", "category": "IT Services", "career_url": "https://dxc.com/careers", "ats_slug": "dxc"},
    {"name": "EPAM Systems", "category": "Digital Engineering", "career_url": "https://epam.com/careers", "ats_slug": "epam"},
    {"name": "Thoughtworks", "category": "Software Consulting", "career_url": "https://thoughtworks.com/careers", "ats_slug": "thoughtworks"},
    {"name": "Globant", "category": "Digital Solutions", "career_url": "https://globant.com/careers", "ats_slug": "globant"},
    {"name": "Endava", "category": "Digital Engineering", "career_url": "https://endava.com/careers", "ats_slug": "endava"},
    {"name": "Luxoft", "category": "Engineering Solutions", "career_url": "https://luxoft.com/careers", "ats_slug": "luxoft"},
    {"name": "Nagarro", "category": "Digital Engineering", "career_url": "https://nagarro.com/careers", "ats_slug": "nagarro"},
    {"name": "Sonata Software", "category": "IT Services", "career_url": "https://sonata-software.com/careers", "ats_slug": "sonata"},
    {"name": "Zensar Technologies", "category": "IT Services", "career_url": "https://zensar.com/careers", "ats_slug": "zensar"},
    {"name": "Happiest Minds", "category": "Digital IT Services", "career_url": "https://happiestminds.com/careers", "ats_slug": "happiestminds"},
    {"name": "Virtusa", "category": "Digital Engineering", "career_url": "https://virtusa.com/careers", "ats_slug": "virtusa"},
    {"name": "UST", "category": "Digital Transformation", "career_url": "https://ust.com/careers", "ats_slug": "ust"},
    {"name": "Tata Technologies", "category": "Engineering Services", "career_url": "https://tatatechnologies.com/careers", "ats_slug": "tatatech"},
    {"name": "Mindteck", "category": "Engineering Software", "career_url": "https://mindteck.com/careers", "ats_slug": "mindteck"},
    {"name": "L&T Technology Services", "category": "Engineering R&D", "career_url": "https://ltts.com/careers", "ats_slug": "ltts"},
    {"name": "CitiusTech", "category": "Healthcare Tech", "career_url": "https://citiustech.com/careers", "ats_slug": "citiustech"},
    {"name": "eClerx", "category": "Data & Process Analytics", "career_url": "https://eclerx.com/careers", "ats_slug": "eclerx"}
]

# Backward compatibility alias
TOP_100_COMPANIES = TOP_200_COMPANIES

# ====================================================================
# 3. Direct ATS Search URL Generator Function
# ====================================================================

def build_direct_job_url(company_name: str, role_title: str, fallback_url: Optional[str] = None) -> str:
    """
    Constructs a direct, pre-filtered search URL into the company's
    actual ATS portal across ALL 200 companies.
    """
    clean_company = company_name.strip().lower()
    clean_role = role_title.strip().replace(" ", "+")
    
    # 1. Custom proprietary search engines (Google, Amazon, Apple, Meta)
    if clean_company in COMPANY_JOB_SEARCH_PATTERNS:
        return COMPANY_JOB_SEARCH_PATTERNS[clean_company].format(role=clean_role)
        
    # 2. Check all 200 companies
    for company in TOP_200_COMPANIES:
        if company["name"].lower() == clean_company:
            slug = company.get("ats_slug", clean_company)
            # If it's a known Greenhouse or Lever company:
            if company.get("category") in ["Fintech", "Developer Tools", "Data / AI"]:
                return f"https://boards.greenhouse.io/{slug}?query={clean_role}"
            return f"{company['career_url']}?q={clean_role}"
            
    # 3. Universal Fallback
    if fallback_url:
        return fallback_url
        
    return f"https://www.google.com/search?q={clean_company}+{clean_role}+jobs"

def build_direct_job_url(company_name: str, role_title: str, fallback_url: Optional[str] = None) -> str:
    """
    Constructs a direct, pre-filtered search URL into the company's
    actual ATS portal so candidates land directly on matching open roles.
    """
    clean_company = company_name.strip().lower()
    clean_role = role_title.strip().replace(" ", "+")
    
    # 1. Check custom deep-search templates
    if clean_company in COMPANY_JOB_SEARCH_PATTERNS:
        return COMPANY_JOB_SEARCH_PATTERNS[clean_company].format(role=clean_role)
        
    # 2. Check top 200 directory for company career URL
    for company in TOP_200_COMPANIES:
        if company["name"].lower() == clean_company:
            return f"{company['career_url']}?q={clean_role}"
            
    # 3. Fallback to provided URL or a clean Google Jobs search query
    if fallback_url:
        return fallback_url
        
    return f"https://www.google.com/search?q={clean_company}+{clean_role}+jobs"


def get_top_companies_directory() -> List[Dict]:
    """Returns the full directory of top tech companies."""
    return TOP_200_COMPANIES
    
# ====================================================================
# 4. Multi-Category Company Classification Engine (6 Industry Sectors)
# ====================================================================

COMPANY_CATEGORIES: Dict[str, str] = {
    "all": "🏢 All Categories",
    "big_tech": "🌐 Big Tech Giants",
    "product_saas": "🚀 Product SaaS & AI",
    "fintech": "💳 Fintech & Payments",
    "european_tech": "🇪🇺 European Tech",
    "indian_unicorns": "🇮🇳 Indian Unicorns",
    "it_services": "🏛️ IT & Engineering Services"
}

# Fast lookup sets for O(1) instantaneous matching
BIG_TECH_COMPANIES = {
    "google", "microsoft", "amazon", "apple", "meta", "netflix", "nvidia",
    "adobe", "salesforce", "oracle", "intel", "amd", "cisco", "ibm",
    "qualcomm", "broadcom", "texas instruments", "sony", "samsung",
    "dell", "hp", "vmware", "sap", "servicenow", "workday"
}

FINTECH_COMPANIES = {
    "stripe", "revolut", "klarna", "adyen", "wise", "n26", "monzo",
    "checkout.com", "robinhood", "coinbase", "chime", "affirm", "plaid",
    "brex", "ramp", "sofi", "ripple", "toast", "bill.com", "marqeta",
    "remitly", "paypal", "visa", "mastercard", "bloomberg", "citadel"
}

EUROPEAN_TECH_COMPANIES = {
    "spotify", "deepmind", "mistral", "mistral ai", "asml", "delivery hero",
    "supercell", "bolt", "personio", "celonis", "king", "rovio",
    "skyscanner", "blablacar", "kry", "wolt", "northvolt", "biontech",
    "arm", "siemens", "bosch", "zalando", "just eat", "hellofresh",
    "booking.com", "trustpilot", "babbel", "soundcloud", "deezer", "infobip", "bitpanda"
}

INDIAN_UNICORNS = {
    "razorpay", "cred", "zomato", "swiggy", "zerodha", "flipkart",
    "phonepe", "paytm", "meesho", "groww", "urban company", "inmobi",
    "postman", "browserstack", "freshworks", "zoho", "pine labs",
    "delhivery", "nykaa", "zepto", "blinkit", "dream11", "policybazaar",
    "ola", "coinswitch", "cars24", "lenskart", "sharechat", "upstox",
    "khatabook", "classplus", "apna", "spinny", "rebel foods", "purplle",
    "mamaearth", "games24x7", "navi", "coindcx", "physicswallah", "pw",
    "unacademy", "leadsquared", "darwinbox", "clevertap", "rapido"
}

IT_SERVICES_COMPANIES = {
    "tcs", "infosys", "wipro", "hcltech", "cognizant", "tech mahindra",
    "ltimindtree", "accenture", "capgemini", "persistent", "mphasis",
    "coforge", "birlasoft", "hexaware", "tata elxsi", "kpit", "cyient",
    "genpact", "dxc", "epam", "thoughtworks", "globant", "endava",
    "luxoft", "nagarro", "sonata", "zensar", "happiest minds", "virtusa",
    "ust", "tatatech", "mindteck", "ltts", "citiustech", "eclerx"
}

def get_company_category(company_name: str) -> str:
    """
    Classifies any company into one of the 6 core tech industry sectors:
    'big_tech', 'product_saas', 'fintech', 'european_tech', 'indian_unicorns', 'it_services'
    """
    clean = company_name.strip().lower()
    
    # 1. Direct Set Lookups (Instantaneous O(1) speed)
    if clean in BIG_TECH_COMPANIES or any(k in clean for k in ["google", "microsoft", "amazon", "apple", "meta", "nvidia"]):
        return "big_tech"
        
    if clean in IT_SERVICES_COMPANIES or any(k in clean for k in ["tcs", "infosys", "wipro", "cognizant", "accenture", "capgemini"]):
        return "it_services"
        
    if clean in FINTECH_COMPANIES or any(k in clean for k in ["stripe", "revolut", "klarna", "wise", "paypal", "paytm", "phonepe"]):
        return "fintech"
        
    if clean in INDIAN_UNICORNS or any(k in clean for k in ["zomato", "swiggy", "zerodha", "cred", "razorpay", "flipkart"]):
        return "indian_unicorns"
        
    if clean in EUROPEAN_TECH_COMPANIES or any(k in clean for k in ["spotify", "deepmind", "asml", "supercell", "bolt"]):
        return "european_tech"
        
    # 2. Check TOP_200_COMPANIES category attribute
    for comp in TOP_200_COMPANIES:
        if comp["name"].lower() == clean:
            cat = comp.get("category", "").lower()
            if "big tech" in cat: return "big_tech"
            if "fintech" in cat: return "fintech"
            if "services" in cat or "it" in cat: return "it_services"
            if "gaming" in cat or "mobility" in cat: return "european_tech"
            return "product_saas"
            
    # Default fallback
    return "product_saas"


def get_company_type(company_name: str) -> str:
    """
    Helper function: maps the 6 categories to broad 'service' or 'product'
    so all automated tests and filters remain 100% backward-compatible.
    """
    cat = get_company_category(company_name)
    return "service" if cat == "it_services" else "product"


# ====================================================================
# 5. Live Recruiter & Hiring Team Discovery Generator
# ====================================================================

def get_recruiter_for_company(company_name: str) -> Dict[str, str]:
    """
    Dynamically generates a live LinkedIn People Search targeting active
    technical recruiters and talent acquisition leads for any company.
    Always 100% fresh with today's real hiring personnel!
    """
    clean_name = company_name.strip()
    formatted_query = clean_name.replace(" ", "+")
    
    return {
        "name": f"Hiring Team @ {clean_name}",
        "title": f"Technical Recruiter @ {clean_name}",
        "linkedin_url": f"https://www.linkedin.com/search/results/people/?keywords=technical+recruiter+{formatted_query}"
    }