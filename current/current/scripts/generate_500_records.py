"""
Script: generate_500_records.py
Description: Generates 500 guaranteed-unique, high-quality news records (250 REAL, 250 FAKE)
             across Technology, Health, Politics, Business, Science, Sports, and Education.
             Appends them to Self-generated.csv, ensuring 0 duplicates and rich linguistic diversity.
"""

import os
import csv
import random
import hashlib
from datetime import datetime, timedelta

random.seed(1337)

CITIES = [
    "New Delhi", "Mumbai", "Bengaluru", "Hyderabad", "Chennai", "Kolkata", "Pune", "Ahmedabad",
    "Jaipur", "Surat", "Lucknow", "Kanpur", "Nagpur", "Indore", "Thane", "Bhopal",
    "Visakhapatnam", "Pimpri-Chinchwad", "Patna", "Vadodara", "Ghaziabad", "Ludhiana",
    "Agra", "Nashik", "Faridabad", "Meerut", "Rajkot", "Varanasi", "Srinagar", "Aurangabad",
    "Dhanbad", "Amritsar", "Navi Mumbai", "Allahabad", "Ranchi", "Howrah", "Coimbatore",
    "Jabalpur", "Gwalior", "Vijayawada", "Jodhpur", "Madurai", "Raipur", "Kota", "Guwahati",
    "Chandigarh", "Solapur", "Hubli-Dharwad", "Bareilly", "Moradabad", "Mysore", "Gurugram"
]

DEPARTMENTS = [
    "Ministry of Electronics and Information Technology", "Department of Science and Technology",
    "Ministry of Health and Family Welfare", "Ministry of Road Transport and Highways",
    "Ministry of Finance", "Department of Space", "Ministry of Education",
    "Ministry of New and Renewable Energy", "Department of Telecommunications",
    "Ministry of Commerce and Industry", "Indian Council of Medical Research",
    "Defence Research and Development Organisation", "Indian Space Research Organisation",
    "Reserve Bank of India", "Securities and Exchange Board of India",
    "Central Pollution Control Board", "Council of Scientific and Industrial Research"
]

COMPANIES = [
    "Tata Consultancy Services", "Infosys Technologies", "Reliance Industries", "Wipro Limited",
    "HCL Technologies", "Bharat Electronics", "Larsen & Toubro", "State Bank of India",
    "Adani Green Energy", "NTPC Limited", "Mahindra & Mahindra", "Sun Pharma",
    "Serum Institute of India", "Bharat Biotech", "Dr. Reddy's Laboratories", "Tech Mahindra"
]

AUTHORS = [
    "Aarav Sharma", "Diya Patel", "Vihaan Rao", "Ananya Deshmukh", "Reyansh Joshi",
    "Saanvi Kulkarni", "Ishaan Verma", "Aanya Nair", "Aditya Iyer", "Mira Banerjee",
    "Kabir Bhatt", "Tanvi Sengupta", "Dhruv Menon", "Riya Pillai", "Arjun Saxena",
    "Pooja Hegde", "Siddharth Jain", "Sneha Kapoor", "Rohan Mehta", "Neha Choudhury"
]

FAKE_SOURCES = [
    "Viral WhatsApp Message", "Social Media Post", "Anonymous Telegram Channel",
    "Unverified Online Blog", "Forwarded Message", "Viral Video Claim",
    "Fake News Portal", "Clickbait Web Forum", "Rumor Network", "Chain Broadcast"
]

REAL_SOURCES = [
    "Press Information Bureau", "Reuters", "Press Trust of India", "Asian News International",
    "The Hindu", "Business Standard", "Economic Times", "Livemint", "Doordarshan News",
    "All India Radio", "Nature India", "Medical News Today", "Financial Express"
]

# Varied topics and sub-templates for REAL news
REAL_GENERATORS = [
    # 1. Tech & AI
    lambda i: {
        "topic": "Technology",
        "title": f"{random.choice(COMPANIES)} Unveils Advanced {random.choice(['AI Computing Architecture', 'Cloud Data Centre', 'Semiconductor Design Lab', '5G Core Network System', 'Cybersecurity Shield'])} in {random.choice(CITIES)}",
        "article_text": f"Leading enterprise {random.choice(COMPANIES)} officially inaugurated an advanced technological facility focusing on {random.choice(['generative artificial intelligence', 'secure hybrid cloud architecture', 'silicon transistor design', 'optical broadband telemetry'])} in {random.choice(CITIES)}. Officials announced an initial capital investment of Rs {random.randint(400, 3500)} crore, aiming to train over {random.randint(2000, 15000)} specialized engineers by next year.",
        "keywords": "Technology, Innovation, Investment, Cloud, Infrastructure"
    },
    # 2. Health & Pharma
    lambda i: {
        "topic": "Health",
        "title": f"Health Authorities Expand Nationwide {random.choice(['Immunization Drive', 'Cancer Screening Initiative', 'Rural Telemedicine Program', 'Dialysis Network', 'Mobile Health Clinic Fleet'])} to {random.randint(25, 95)} Districts",
        "article_text": f"The {random.choice(DEPARTMENTS)} confirmed the formal expansion of its primary healthcare initiative to over {random.randint(25, 95)} underserved rural districts across the nation. Under this program, certified medical practitioners will deploy standardized diagnostic protocols and subsidized medicines, targeting an estimated beneficiary population of {random.randint(3, 18)} lakh citizens.",
        "keywords": "Healthcare, Medicine, Public Health, Rural, Treatment"
    },
    # 3. Governance & Policy
    lambda i: {
        "topic": "Politics",
        "title": f"{random.choice(DEPARTMENTS)} Approves National Framework for {random.choice(['Sustainable Urban Transit', 'Agricultural Digitization', 'Inland Waterway Logistics', 'Green Hydrogen Export', 'Semiconductor Subsidies', 'Digital Infrastructure', 'Rural Electrification'])} in {random.choice(CITIES)}",
        "article_text": f"In a cabinet meeting chaired in New Delhi, the Union Government approved a comprehensive development policy to modernize {random.choice(['interstate transport logistics', 'precision agricultural supply chains', 'clean hydrogen production hubs', 'electronic manufacturing clusters'])}. The framework allocates Rs {random.randint(1200, 9500)} crore over a five-year implementation period with clear performance milestones.",
        "keywords": "Government, Policy, Cabinet, Economy, Reform"
    },
    # 4. Finance & Economy
    lambda i: {
        "topic": "Business",
        "title": f"{random.choice(['Reserve Bank of India', 'Securities and Exchange Board of India', 'Ministry of Finance'])} Issues Updated Guidelines for {random.choice(['Digital Payment Security', 'Corporate Governance Standards', 'SME Export Credit', 'Algorithmic Trading Audits', 'Retail Investor Safeguards'])}",
        "article_text": f"The monetary regulatory authority released a circular mandating stringent operational guidelines for institutions offering {random.choice(['instant merchant transactions', 'cross-border remittances', 'small enterprise lines of credit', 'automated equity trading'])}. Regulated entities have been granted a transition period of {random.randint(60, 180)} days to implement enhanced audit mechanisms and real-time fraud monitoring systems.",
        "keywords": "Finance, Economy, Banking, Regulation, Markets"
    },
    # 5. Science & Space
    lambda i: {
        "topic": "Science",
        "title": f"Scientific Team at {random.choice(DEPARTMENTS)} Achieves Breakthrough in {random.choice(['High-Efficiency Solar Photovoltaics', 'Bio-Degradable Polymer Synthesis', 'Cryogenic Propulsion Testing', 'Quantum Key Distribution', 'Drought-Resistant Crop Strains'])}",
        "article_text": f"A dedicated research cohort supported by the {random.choice(DEPARTMENTS)} successfully demonstrated a technical milestone in {random.choice(['solar cell energy conversion efficiency', 'ambient-temperature quantum encryption', 'cryogenic engine propellant mixture ratio', 'enzymatic plastic decomposition'])}. The empirical findings, peer-reviewed and published this week, confirm operational stability under rigorous testing parameters in {random.choice(CITIES)}.",
        "keywords": "Science, Research, Technology, Innovation, Laboratory"
    },
    # 6. Infrastructure & Environment
    lambda i: {
        "topic": "Infrastructure",
        "title": f"New {random.randint(40, 180)}-Kilometre {random.choice(['Expressway Corridor', 'High-Speed Railway Link', 'Freight Transit Bypass', 'Metro Phase Corridor'])} Inaugurated Near {random.choice(CITIES)}",
        "article_text": f"Transport authorities commenced official vehicular movement along the newly completed {random.randint(40, 180)}-kilometre transit corridor connecting {random.choice(CITIES)} with regional agricultural hubs. The infrastructure project is projected to slash peak travel duration by {random.randint(30, 65)} percent while integrating advanced automated toll systems and ecological wildlife crossings.",
        "keywords": "Infrastructure, Transport, Transit, Regional Development"
    },
    # 7. Education & Sports
    lambda i: {
        "topic": "Education",
        "title": f"National Council Launches Standardized Curriculum for {random.choice(['Artificial Intelligence and Robotics', 'Renewable Energy Systems', 'Data Science and Analytics', 'Environmental Sustainability', 'Vocational Trades'])} in {random.randint(150, 800)} Colleges",
        "article_text": f"The academic curriculum regulatory body announced the integration of industry-certified coursework covering {random.choice(['applied machine learning', 'clean energy grid maintenance', 'statistical data engineering', 'cyber defense essentials'])} across {random.randint(150, 800)} undergraduate institutions. The curriculum was co-designed with premier technology enterprises to elevate graduate employability.",
        "keywords": "Education, University, Curriculum, Students, Skills"
    },
    # 8. Sports
    lambda i: {
        "topic": "Sports",
        "title": f"National {random.choice(['Archery', 'Shooting', 'Badminton', 'Athletics', 'Weightlifting', 'Chess'])} Contingent Wins {random.randint(4, 18)} Medals at International Championship",
        "article_text": f"National athletes delivered an exceptional performance at the international athletic championship in Asia, claiming a cumulative haul of {random.randint(4, 18)} medals including {random.randint(2, 7)} golds. Sports ministry administrators announced monetary felicitations and modern training infrastructure upgrades for the victorious squad.",
        "keywords": "Sports, Medals, Athletics, Championship, Victory"
    }
]

# Varied topics and sub-templates for FAKE news
FAKE_GENERATORS = [
    # 1. Tech Panic & Conspiracies
    lambda i: {
        "topic": "Technology",
        "title": f"Viral Claim Asserts {random.choice(['New 5G Towers', 'Smart Electric Meters', 'Wi-Fi Routers', 'Bluetooth Headsets', 'Digital CCTV Cameras'])} in {random.choice(CITIES)} Emit {random.choice(['Harmful Mind-Control Waves', 'Secret DNA-Altering Frequencies', 'Dangerous Micro-Radiation', 'Hidden Behavioral Signals'])}",
        "article_text": f"An unverified audio clip circulating on social messaging groups falsely claimed that newly installed {random.choice(['cellular antennas', 'smart electronic energy meters', 'wireless routers'])} in {random.choice(CITIES)} are secretly transmitting experimental frequency bands that disrupt human brainwaves. Regulatory telecom agencies and certified acoustic physicists categorically refuted the rumor, confirming emissions remain well within global biological safety limits.",
        "keywords": "Viral, Hoax, Technology, Conspiracy, Fake"
    },
    # 2. Medical Miracle Cures
    lambda i: {
        "topic": "Health",
        "title": f"Deceptive Post in {random.choice(CITIES)} Claims Boiling {random.choice(['Papaya Seeds with Ginger', 'Neem Bark with Lemon', 'Guava Leaves with Turmeric', 'Fenugreek with Garlic Juice', 'Bitter Gourd with Honey'])} Cures {random.choice(['Stage 4 Cancer', 'Chronic Kidney Disease', 'Severe Cardiac Blockages', 'Type 1 Diabetes', 'Liver Cirrhosis'])} in {random.randint(4, 21)} Days",
        "article_text": f"A deceptive viral video spreading across social media in {random.choice(CITIES)} falsely asserted that drinking boiled extracts of {random.choice(['papaya seeds and ginger', 'neem bark and lemon', 'herbal roots and honey', 'bitter gourd with raw turmeric', 'clove oil with cinnamon'])} completely cures {random.choice(['malignant tumors', 'chronic renal dysfunction', 'arterial plaque blockages', 'advanced diabetes', 'autoimmune disorders'])} without hospital intervention in {random.randint(3, 21)} days. Leading oncologists in {random.choice(CITIES)} warned that abandoning proven medical therapy is life-threatening.",
        "keywords": "Health Hoax, Miracle Cure, Pseudoscience, Medical Scam"
    },
    # 3. Banking & Currency Scams
    lambda i: {
        "topic": "Business",
        "title": f"Fake Message Claims {random.choice(['All ATM Withdrawals Banned', 'Bank Accounts Below Rs 10000 Frozen', 'Currency Notes with Pen Marks Invalid', '50 Percent Tax on Digital Transfers', 'Savings Account Interest Cancelled'])} Starting Tomorrow Across {random.choice(CITIES)}",
        "article_text": f"Alarmist chain forwards distributed through messaging platforms in {random.choice(CITIES)} falsely asserted that monetary authorities have ordered commercial banks to {random.choice(['freeze consumer accounts with low balances', 'refuse currency notes bearing ink marks', 'levy an emergency 50 percent penalty on digital remittances', 'deactivate savings debit cards'])} starting from midnight. Banking spokespersons in {random.choice(CITIES)} debunked the fabricated message and advised the public to disregard unauthorized financial panic messages.",
        "keywords": "Banking Scam, Currency Hoax, Panic, Finance, Fake Alert"
    },
    # 4. Government Tax & Banning Rumors
    lambda i: {
        "topic": "Politics",
        "title": f"Fabricated Circular Claims Government Imposing {random.randint(20, 45)} Percent Emergency Surcharge on {random.choice(['Online Food Delivery', 'Two-Wheeler Purchases', 'Domestic Mobile Recharges', 'LPG Gas Refills', 'Social Media Messaging', 'Electricity Bills', 'Internet Subscriptions'])} in {random.choice(CITIES)}",
        "article_text": f"A forged government notification bearing a counterfeit ministry crest alleged that the treasury has implemented a new emergency tax of {random.randint(20, 45)} percent on everyday {random.choice(['grocery delivery services', 'mobile phone recharges', 'domestic fuel cylinders', 'internet broadband services'])} in {random.choice(CITIES)}. Fact-checking bureaus confirmed the circulating document is a complete fabrication with no legal or administrative basis.",
        "keywords": "Tax Hoax, Forgery, Government, Fake Notification, Rumor"
    },
    # 5. Phishing & Cash Subsidy Scams
    lambda i: {
        "topic": "Business",
        "title": f"Phishing Alert in {random.choice(CITIES)} as Fraudulent Post Promises Free Rs {random.choice(['25,000', '50,000', '75,000', '1,00,000', '1,50,000'])} {random.choice(['Student Laptop Grant', 'Youth Unemployment Bonus', 'Festival Welfare Allowance', 'Solar Subsidy Transfer', 'Digital Tablet Scheme'])}",
        "article_text": f"Malicious links circulated on group chats in {random.choice(CITIES)} falsely claimed that the central welfare department is giving out direct bank transfers of Rs {random.choice(['25,000', '50,000', '75,000', '1,00,000'])} to every applicant who registers their mobile OTP and banking credentials on an unknown portal. Cyber police units in {random.choice(CITIES)} issued an urgent red alert, identifying the scheme as an automated phishing fraud.",
        "keywords": "Phishing, Scam, Fake Grant, Financial Fraud, Cyber Crime"
    },
    # 6. Bizarre Planetary & Environmental Hoaxes
    lambda i: {
        "topic": "Science",
        "title": f"Sensational Post Claims {random.choice(['Night Moon Will Turn Pitch Black', 'Solar Flare Will Erase All Phone Memories', 'Earth Will Lose Gravity for 15 Minutes', 'Comet Will Cause Global 7-Day Darkness', 'Planetary Convergence Will Trigger Tidal Waves'])} Over {random.choice(CITIES)} on {random.choice(['Friday Night', 'Next Full Moon', 'Upcoming Solar Eclipse', 'Next Weekend'])}",
        "article_text": f"Sensationalist blog pages claimed that an impending cosmic phenomenon on {random.choice(['Friday night', 'the upcoming eclipse', 'next weekend'])} will cause {random.choice(['the moon to completely disappear', 'electromagnetic waves to wipe all smartphone chips', 'terrestrial gravity to temporarily cease', 'total darkness for seven continuous days'])} over {random.choice(CITIES)}. Senior space research scientists refuted the absurd viral claim, assuring the public that no such astronomical anomaly can occur under planetary physical laws.",
        "keywords": "Astronomy Hoax, Space Myth, Viral Claim, Pseudoscience, Hoax"
    },
    # 7. Examination & Education Rumors
    lambda i: {
        "topic": "Education",
        "title": f"Fake Notification Claims {random.choice(['All Board Exams Cancelled', 'College Degree Exams Made Optional', 'Passing Marks Reduced to 20 Percent', 'University Admissions Postponed Indefinitely'])} Across {random.choice(CITIES)} Due to {random.choice(['Server Outages', 'Paper Printing Errors', 'Administrative Strikes'])}",
        "article_text": f"A doctored screenshot impersonating the national education council falsely stated that upcoming examinations across {random.choice(CITIES)} have been {random.choice(['scrapped entirely', 'postponed indefinitely', 'modified with 20 percent passing criteria'])} for over {random.randint(5000, 45000)} students. Examination controllers in {random.choice(CITIES)} urged candidates to ignore fraudulent screenshots and verify scheduling exclusively through certified university portals.",
        "keywords": "Exam Hoax, Student Rumor, Forgery, Education, Misinformation"
    },
    # 8. Celebrity & Sports Hoaxes
    lambda i: {
        "topic": "Sports",
        "title": f"Viral Rumor Falsely Claims {random.choice(['National Cricket Final Cancelled', 'Star Athlete Banned for Lifetime', 'International Tournament Boycotted', 'Championship Venue Shifted Overnight'])} Before {random.choice(CITIES)} Match",
        "article_text": f"Unverified claims circulating on social media in {random.choice(CITIES)} alleged that sports governing federations had abruptly {random.choice(['called off the championship final', 'disqualified premier national players', 'decided to boycott international competitions', 'relocated the stadium venue'])} scheduled in {random.choice(CITIES)}. Official sporting spokespersons clarified that match fixtures remain unchanged and condemned the baseless gossip designed to generate ad clicks.",
        "keywords": "Sports Hoax, Clickbait, Rumor, Disinformation, Cricket"
    }
]

def compute_hash(text):
    return hashlib.sha256(text.encode("utf-8")).hexdigest()

def main():
    target_csv = "F:\\Fake news detection\\Self-generated.csv"
    if not os.path.exists(target_csv):
        print(f"[ERROR] Target file not found at {target_csv}")
        return

    # 1. Read existing records
    existing_rows = []
    seen_hashes = set()
    seen_titles = set()
    seen_articles = set()

    with open(target_csv, "r", encoding="utf-8-sig") as f:
        reader = csv.DictReader(f)
        fieldnames = reader.fieldnames
        for r in reader:
            existing_rows.append(r)
            norm = (r["title"].strip().lower() + " " + r.get("article_text", "").strip().lower())
            seen_hashes.add(compute_hash(norm))
            seen_titles.add(r["title"].strip().lower())
            seen_articles.add(r.get("article_text", "").strip().lower())

    initial_count = len(existing_rows)
    print(f"Existing records in Self-generated.csv: {initial_count}")
    print(f"Unique existing content hashes: {len(seen_hashes)}")

    # We want exactly 500 new unique records: 250 Real, 250 Fake
    new_records = []
    
    # Generate 250 unique REAL
    real_generated = 0
    attempts = 0
    while real_generated < 250 and attempts < 30000:
        attempts += 1
        gen_fn = random.choice(REAL_GENERATORS)
        item = gen_fn(real_generated)
        title_lower = item["title"].strip().lower()
        art_lower = item["article_text"].strip().lower()
        norm = (title_lower + " " + art_lower)
        h = compute_hash(norm)
        if h in seen_hashes or title_lower in seen_titles or art_lower in seen_articles:
            continue
        seen_hashes.add(h)
        seen_titles.add(title_lower)
        seen_articles.add(art_lower)

        days_offset = random.randint(1, 300)
        pub_date = (datetime(2026, 1, 1) + timedelta(days=days_offset)).strftime("%m/%d/%Y")
        author = random.choice(AUTHORS)
        source = random.choice(REAL_SOURCES)
        rec_idx = initial_count + len(new_records) + 1

        rec = {
            "news_id": f"NEWS{rec_idx:06d}",
            "title": item["title"],
            "article_text": item["article_text"],
            "source": source,
            "topic": item["topic"],
            "author": author,
            "published_date": pub_date,
            "language": "English",
            "country": "India",
            "news_type": "Previous",
            "keywords": item["keywords"],
            "label": 1,
            "label_name": "Real",
            "Unnamed: 13": ""
        }
        new_records.append(rec)
        real_generated += 1

    print(f"Generated {real_generated} guaranteed-unique REAL records.")

    # Generate 250 unique FAKE
    fake_generated = 0
    attempts = 0
    while fake_generated < 250 and attempts < 30000:
        attempts += 1
        gen_fn = random.choice(FAKE_GENERATORS)
        item = gen_fn(fake_generated)
        title_lower = item["title"].strip().lower()
        art_lower = item["article_text"].strip().lower()
        norm = (title_lower + " " + art_lower)
        h = compute_hash(norm)
        if h in seen_hashes or title_lower in seen_titles or art_lower in seen_articles:
            continue
        seen_hashes.add(h)
        seen_titles.add(title_lower)
        seen_articles.add(art_lower)

        days_offset = random.randint(1, 300)
        pub_date = (datetime(2026, 1, 1) + timedelta(days=days_offset)).strftime("%m/%d/%Y")
        author = "Anonymous Social Media User"
        source = random.choice(FAKE_SOURCES)
        rec_idx = initial_count + len(new_records) + 1

        rec = {
            "news_id": f"NEWS{rec_idx:06d}",
            "title": item["title"],
            "article_text": item["article_text"],
            "source": source,
            "topic": item["topic"],
            "author": author,
            "published_date": pub_date,
            "language": "English",
            "country": "India",
            "news_type": "Previous",
            "keywords": item["keywords"],
            "label": 0,
            "label_name": "Fake",
            "Unnamed: 13": ""
        }
        new_records.append(rec)
        fake_generated += 1

    print(f"Generated {fake_generated} guaranteed-unique FAKE records.")

    all_rows = existing_rows + new_records
    print(f"Total records in combined pool: {len(all_rows)}")

    cleaned_fieldnames = [c for c in fieldnames if c and c.strip()]
    with open(target_csv, "w", newline="", encoding="utf-8") as f:
        writer = csv.DictWriter(f, fieldnames=cleaned_fieldnames, extrasaction="ignore")
        writer.writeheader()
        for r in all_rows:
            writer.writerow(r)

    print(f"[SUCCESS] Wrote {len(all_rows)} total records into {target_csv}.")

if __name__ == "__main__":
    main()
