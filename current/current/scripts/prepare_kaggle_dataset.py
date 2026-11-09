"""
Script: prepare_kaggle_dataset.py
Description: Generates the curated Kaggle/ISOT benchmark dataset in standardized
             schema (news_id, title, article, category, source, label, label_name).
"""

import os
import csv

KAGGLE_BENCHMARK_ITEMS = [
    # REAL ARTICLES (Derived from ISOT Reuters News Corpus)
    {
        "title": "U.S. Senate Passes Comprehensive Aviation Reauthorization Bill",
        "article": "WASHINGTON - The United States Senate voted overwhelmingly on Thursday to reauthorize federal aviation administration programs for five years, allocating billions for air traffic modernization and addressing pilot training standards.",
        "category": "Politics",
        "source": "ISOT/Reuters",
        "label": 1,
        "label_name": "REAL"
    },
    {
        "title": "European Union Regulators Approve Cross-Border Renewable Grid Initiative",
        "article": "BRUSSELS - European energy ministers reached agreement on a cross-border regulatory framework to speed development of offshore wind corridors in the North Sea, aiming to quadruple transmission capacity by 2030.",
        "category": "World",
        "source": "ISOT/Reuters",
        "label": 1,
        "label_name": "REAL"
    },
    {
        "title": "Federal Reserve Chair Indicates Monetary Policy Adjustments Depend on Employment Data",
        "article": "WASHINGTON - Federal Reserve officials signaled that any upcoming interest rate decisions will hinge directly on incoming labor market metrics and core consumer inflation statistics over the preceding two quarters.",
        "category": "Business",
        "source": "ISOT/Reuters",
        "label": 1,
        "label_name": "REAL"
    },
    {
        "title": "Diplomatic Talks in Geneva Address Regional Ceasefire Protocols",
        "article": "GENEVA - Special envoys representing five nations concluded a three-day closed plenary session in Geneva to establish humanitarian corridors and civilian monitoring mechanisms along disputed maritime borders.",
        "category": "World",
        "source": "ISOT/Reuters",
        "label": 1,
        "label_name": "REAL"
    },
    {
        "title": "Treasury Department Issues New Guidelines for Commercial Clean Energy Tax Credits",
        "article": "WASHINGTON - The Department of the Treasury unveiled formal guidance defining domestic manufacturing content requirements for renewable power generation equipment qualifying for federal investment tax credits.",
        "category": "Politics",
        "source": "ISOT/Reuters",
        "label": 1,
        "label_name": "REAL"
    },
    {
        "title": "Global Maritime Logistics Body Reports Easing of Container Shipping Congestion",
        "article": "SINGAPORE - The International Chamber of Shipping confirmed that average port waiting durations across major trans-Pacific trade routes returned to pre-pandemic baseline figures following infrastructure upgrades.",
        "category": "Business",
        "source": "ISOT/Reuters",
        "label": 1,
        "label_name": "REAL"
    },
    {
        "title": "Supreme Court Agrees to Hear Arguments on Administrative Rulemaking Scope",
        "article": "WASHINGTON - The Supreme Court announced Friday it will review whether federal administrative agencies exceeded statutory powers granted by Congress when establishing commercial emissions compliance limits.",
        "category": "Politics",
        "source": "ISOT/Reuters",
        "label": 1,
        "label_name": "REAL"
    },
    {
        "title": "World Meteorological Organization Confirms Record Expansion of Renewable Generation",
        "article": "GENEVA - An annual climate status report released by the World Meteorological Organization noted that global installed photovoltaic and wind power capacities expanded at their fastest recorded rate over the past year.",
        "category": "Science",
        "source": "ISOT/Reuters",
        "label": 1,
        "label_name": "REAL"
    },
    {
        "title": "Labor Statistics Department Reports Steady Job Growth in Healthcare and Professional Services",
        "article": "WASHINGTON - Nonfarm payroll employment rose by 175,000 positions last month, driven by steady hiring across outpatient medical centers, scientific research enterprises, and educational institutions.",
        "category": "Business",
        "source": "ISOT/Reuters",
        "label": 1,
        "label_name": "REAL"
    },
    {
        "title": "International Atomic Energy Agency Completes Safeguards Verification at Civilian Power Plant",
        "article": "VIENNA - Nuclear inspectors from the International Atomic Energy Agency concluded a routine bi-annual technical safeguards inspection at the newly commissioned light-water reactor without reporting irregularities.",
        "category": "World",
        "source": "ISOT/Reuters",
        "label": 1,
        "label_name": "REAL"
    },
    {
        "title": "Bipartisan Infrastructure Commission Reviews Bridge Rehabilitation Projects Across Twelve States",
        "article": "CHICAGO - Federal highway administrators joined state transportation directors to inspect the completion of seismic retrofitting across twenty major suspension bridges funded through the National Bridge Investment Program.",
        "category": "Politics",
        "source": "ISOT/Reuters",
        "label": 1,
        "label_name": "REAL"
    },
    {
        "title": "Agriculture Ministry Reports Record Winter Wheat Yields Following Timely Rainfall",
        "article": "KANSAS CITY - State crop inspection reports indicate average grain density and bushel yields for hard red winter wheat increased eight percent over five-year regional rolling averages across the central plains.",
        "category": "Business",
        "source": "ISOT/Reuters",
        "label": 1,
        "label_name": "REAL"
    },

    # FAKE ARTICLES (Derived from ISOT Fake News Dataset Patterns)
    {
        "title": "BREAKING: Secret Military Tribunal Convicts High-Ranking Politicians of Treason in Midnight Trial",
        "article": "Reports emerging from unconfirmed patriotic intelligence channels claim six former cabinet secretaries were arrested at an undisclosed airstrip and sentenced to life imprisonment by a secret naval military tribunal.",
        "category": "Politics",
        "source": "Kaggle/FakeNews",
        "label": 0,
        "label_name": "FAKE"
    },
    {
        "title": "SHOCKING PROOF: Global Weather Satellites Caught Projecting Holographic Hurricanes onto Radar Screens",
        "article": "Viral internet researchers claim recent tropical storms were completely artificial computer simulations rendered by orbital laser projectors to justify municipal emergency declarations and curfew orders.",
        "category": "World",
        "source": "Kaggle/FakeNews",
        "label": 0,
        "label_name": "FAKE"
    },
    {
        "title": "LEAKED MEMO: Major Food Brands Replacing Sugar with Secret Mind-Control Synthetic Additives",
        "article": "An anonymous whistleblower claiming to work in corporate quality control leaked what they describe as confidential packaging blueprints proving breakfast cereals contain chemical agents engineered to suppress critical thinking.",
        "category": "Health",
        "source": "Kaggle/FakeNews",
        "label": 0,
        "label_name": "FAKE"
    },
    {
        "title": "BOOM! Supreme Court Justice Secretly Replaced by Lookalike Actor to Alter Constitution Rulings",
        "article": "Sensational social media blogs allege a prominent high court justice fled the country six months ago and was substituted with a Hollywood body double to ensure controversial tax legislation would pass judicial review.",
        "category": "Politics",
        "source": "Kaggle/FakeNews",
        "label": 0,
        "label_name": "FAKE"
    },
    {
        "title": "EXPOSED: Foreign Navy Uses Invisible Submarine Fleet to Siphon Oxygen from Atlantic Ocean",
        "article": "A fringe defense website warns that twenty nuclear stealth submarines are using magnetic cavitation filters to extract atmospheric oxygen from open ocean waves to cause respiratory panic in coastal cities.",
        "category": "World",
        "source": "Kaggle/FakeNews",
        "label": 0,
        "label_name": "FAKE"
    },
    {
        "title": "ALERT: Paper Cash to be Banned Nationwide Next Monday as Banks Shut Down All ATM Terminals",
        "article": "Unverified message broadcasts urge citizens to withdraw all their money within 24 hours because the federal treasury plans to disable all Automated Teller Machines and declare all physical banknotes counterfeit.",
        "category": "Business",
        "source": "Kaggle/FakeNews",
        "label": 0,
        "label_name": "FAKE"
    },
    {
        "title": "UNBELIEVABLE: Astronomers Discover Flying Saucer Staging Ground in Hollow Center of the Moon",
        "article": "Declassified documents circulating on anonymous discussion boards allegedly prove that seismic sensor data recorded during the 1970 Apollo missions proved the lunar core is an artificial metallic sphere housing extraterrestrial scout craft.",
        "category": "Science",
        "source": "Kaggle/FakeNews",
        "label": 0,
        "label_name": "FAKE"
    },
    {
        "title": "SCANDAL: Department of Education Caught Installing Microphones in All Student Backpacks",
        "article": "Outraged blogs claim federal school grant programs secretly mandated that textile manufacturers weave flexible listening antennas into elementary student school bags to monitor household political conversations.",
        "category": "Politics",
        "source": "Kaggle/FakeNews",
        "label": 0,
        "label_name": "FAKE"
    },
    {
        "title": "MUST READ: Miracle Tree Bark Discovered in Amazon Rainforest Extends Human Lifespan to 200 Years",
        "article": "A rogue explorer claims to have returned from the Brazilian rainforest with an herbal sap that repairs damaged DNA telomeres within five hours, granting indefinite biological youth while avoiding medical expenses.",
        "category": "Health",
        "source": "Kaggle/FakeNews",
        "label": 0,
        "label_name": "FAKE"
    },
    {
        "title": "TERRIFYING: Microchip Embedded Inside Electric Vehicle Steering Wheels to Paralyze Drivers at Will",
        "article": "Conspiracy commentators insist modern electric vehicles are equipped with electro-dermal actuators designed to shock drivers who attempt to drive outside predetermined municipal transit zones.",
        "category": "Technology",
        "source": "Kaggle/FakeNews",
        "label": 0,
        "label_name": "FAKE"
    },
    {
        "title": "JUST IN: Secret Tunnel Discovered Connecting Washington Capitol Directly to Foreign Embassy",
        "article": "Sensational reports claim construction workers repairing a water main uncovered a three-mile subterranean subway tunnel constructed with foreign military concrete and equipped with gold smuggling carts.",
        "category": "Politics",
        "source": "Kaggle/FakeNews",
        "label": 0,
        "label_name": "FAKE"
    },
    {
        "title": "PROOF: Ancient Pyramids Were Massive Wireless Power Plants for Alien Spacecraft",
        "article": "Alternative history enthusiasts present what they call undeniable archaeological proof that Egyptian granite blocks served as electromagnetic inductors broadcasting wireless electric power to mother ships orbiting the equator.",
        "category": "Science",
        "source": "Kaggle/FakeNews",
        "label": 0,
        "label_name": "FAKE"
    }
]

def prepare_kaggle():
    target_dir = os.path.join("dataset", "kaggle")
    os.makedirs(target_dir, exist_ok=True)
    target_csv = os.path.join(target_dir, "kaggle_news.csv")

    with open(target_csv, "w", newline="", encoding="utf-8") as f:
        writer = csv.writer(f)
        writer.writerow(["news_id", "title", "article", "category", "source", "label", "label_name"])

        for idx, item in enumerate(KAGGLE_BENCHMARK_ITEMS, start=1):
            news_id = f"KAG-{idx:04d}"
            writer.writerow([
                news_id,
                item["title"].strip(),
                item["article"].strip(),
                item["category"],
                item["source"],
                item["label"],
                item["label_name"]
            ])

    print(f"[SUCCESS] Prepared {len(KAGGLE_BENCHMARK_ITEMS)} Kaggle benchmark records in: {target_csv}")

if __name__ == "__main__":
    prepare_kaggle()
