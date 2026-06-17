import re
import requests
from playwright.sync_api import sync_playwright

ALERT_WEBHOOK = "https://discord.com/api/webhooks/1516297935154053243/Vr0mCI2ivgG9QCasszBzXfECv-tU6ZkthszOswnyUxDh7Qw06h4j71fVTunMnVELtLIG"
POTENTIAL_WEBHOOK = "https://discord.com/api/webhooks/1516490766954795062/TpGAGZxJxh2LraSpQm9o1ZXL7vjcIIIf0vMn9UfQZ3iZgw2z496l7KSiSXwbUIpdUn9d"

LEFTY_WORDS = [
    "left",
    "lefty",
    "left-handed",
    "left handed",
    "lh"
]

SEEN_FILE = "seen_links.txt"
BAD_KEYWORDS_FILE = "bad_keywords.txt"

SEARCHES = {
    "Reverb Left-Handed Category": "https://reverb.com/marketplace?product_type=electric-guitars&category=left-handed&sort=published_at%7Cdesc",
    "Reverb Left Keyword": "https://reverb.com/marketplace?query=left&product_type=electric-guitars&sort=published_at%7Cdesc",
    
    "ESP Horizon": "https://reverb.com/marketplace?query=esp%20horizon%20left&product_type=electric-guitars&condition=used&sort=published_at%7Cdesc",
    "ESP Viper": "https://reverb.com/marketplace?query=esp%20viper%20left&product_type=electric-guitars&condition=used&sort=published_at%7Cdesc",
    "ESP Mirage": "https://reverb.com/marketplace?query=esp%20mirage%20left&product_type=electric-guitars&condition=used&sort=published_at%7Cdesc",
    "ESP M-I": "https://reverb.com/marketplace?query=esp%20m-i%20left&product_type=electric-guitars&condition=used&sort=published_at%7Cdesc",
    "ESP M-II": "https://reverb.com/marketplace?query=esp%20m-ii%20left&product_type=electric-guitars&condition=used&sort=published_at%7Cdesc",
    "ESP Snapper": "https://reverb.com/marketplace?query=esp%20snapper%20left&product_type=electric-guitars&condition=used&sort=published_at%7Cdesc",
    "ESP Star": "https://reverb.com/marketplace?query=esp%20star%20left&product_type=electric-guitars&condition=used&sort=published_at%7Cdesc",
    "ESP Eclipse": "https://reverb.com/marketplace?query=esp%20eclipse%20left&product_type=electric-guitars&condition=used&sort=published_at%7Cdesc",
    "ESP Throbber": "https://reverb.com/marketplace?query=esp%20throbber%20left&product_type=electric-guitars&condition=used&sort=published_at%7Cdesc",
    "ESP Custom": "https://reverb.com/marketplace?query=esp%20custom%20left&product_type=electric-guitars&condition=used&sort=published_at%7Cdesc",

    "Jackson Kelly": "https://reverb.com/marketplace?query=jackson%20kelly%20left&product_type=electric-guitars&condition=used&sort=published_at%7Cdesc",
    "Jackson KE": "https://reverb.com/marketplace?query=jackson%20ke%20left&product_type=electric-guitars&condition=used&sort=published_at%7Cdesc",
    "Jackson RR": "https://reverb.com/marketplace?query=jackson%20rr%20left&product_type=electric-guitars&condition=used&sort=published_at%7Cdesc",
    "Jackson KV": "https://reverb.com/marketplace?query=jackson%20kv%20left&product_type=electric-guitars&condition=used&sort=published_at%7Cdesc",
    "Jackson Soloist": "https://reverb.com/marketplace?query=jackson%20soloist%20left&product_type=electric-guitars&condition=used&sort=published_at%7Cdesc",

    "Music Man Petrucci": "https://reverb.com/marketplace?query=music%20man%20john%20petrucci%20left&product_type=electric-guitars&condition=used&sort=published_at%7Cdesc",
    "Music Man JP7": "https://reverb.com/marketplace?query=music%20man%20jp7%20left&product_type=electric-guitars&condition=used&sort=published_at%7Cdesc",
    "Music Man JP6": "https://reverb.com/marketplace?query=music%20man%20jp6%20left&product_type=electric-guitars&condition=used&sort=published_at%7Cdesc",
    "Music Man Luke": "https://reverb.com/marketplace?query=music%20man%20luke%20left&product_type=electric-guitars&condition=used&sort=published_at%7Cdesc",
    "Music Man Axis": "https://reverb.com/marketplace?query=music%20man%20axis%20left&product_type=electric-guitars&condition=used&sort=published_at%7Cdesc",

    "Charvel": "https://reverb.com/marketplace?query=charvel%20left&product_type=electric-guitars&condition=used&sort=published_at%7Cdesc",
    "Gibson": "https://reverb.com/marketplace?query=gibson%20left&product_type=electric-guitars&condition=used&sort=published_at%7Cdesc",
    "Ibanez": "https://reverb.com/marketplace?query=ibanez%20left&product_type=electric-guitars&condition=used&sort=published_at%7Cdesc",
    "Edwards": "https://reverb.com/marketplace?query=edwards%20left&product_type=electric-guitars&condition=used&sort=published_at%7Cdesc",
    "Kiesel": "https://reverb.com/marketplace?query=kiesel%20left&product_type=electric-guitars&condition=used&sort=published_at%7Cdesc",
    "Carvin": "https://reverb.com/marketplace?query=carvin%20left&product_type=electric-guitars&condition=used&sort=published_at%7Cdesc",
    "Fender USA": "https://reverb.com/marketplace?query=fender%20usa%20left&product_type=electric-guitars&condition=used&sort=published_at%7Cdesc",
    "Performance": "https://reverb.com/marketplace?query=performance%20left&product_type=electric-guitars&condition=used&sort=published_at%7Cdesc",
    "Rickenbacker": "https://reverb.com/marketplace?query=rickenbacker%20left&product_type=electric-guitars&condition=used&sort=published_at%7Cdesc",
    "BC Rich": "https://reverb.com/marketplace?query=bc%20rich%20left&product_type=electric-guitars&condition=used&sort=published_at%7Cdesc",
    "Washburn": "https://reverb.com/marketplace?query=washburn%20left&product_type=electric-guitars&condition=used&sort=published_at%7Cdesc",
    "Dean": "https://reverb.com/marketplace?query=dean%20left&product_type=electric-guitars&condition=used&sort=published_at%7Cdesc",
    "Kramer": "https://reverb.com/marketplace?query=kramer%20left&product_type=electric-guitars&condition=used&sort=published_at%7Cdesc",
    "PRS Custom": "https://reverb.com/marketplace?query=prs%20custom%20left&product_type=electric-guitars&condition=used&sort=published_at%7Cdesc",
    "EVH": "https://reverb.com/marketplace?query=evh%20left&product_type=electric-guitars&condition=used&sort=published_at%7Cdesc",
    "Gretsch": "https://reverb.com/marketplace?query=gretsch%20left&product_type=electric-guitars&condition=used&sort=published_at%7Cdesc",
    "Schecter Signature": "https://reverb.com/marketplace?query=schecter%20signature%20left&product_type=electric-guitars&condition=used&sort=published_at%7Cdesc",
}


def load_file_lines(filename):
    try:
        with open(filename, "r", encoding="utf-8") as file:
            return set(line.strip().lower() for line in file if line.strip())
    except FileNotFoundError:
        return set()


def save_seen_link(link):
    with open(SEEN_FILE, "a", encoding="utf-8") as file:
        file.write(link + "\n")


def clean_link(link):
    if link.startswith("/"):
        link = "https://reverb.com" + link
    return link.split("?")[0]


def is_bad_suggestion(title, bad_keywords):
    title_lower = title.lower()
    for keyword in bad_keywords:
        if keyword in title_lower:
            return True, keyword
    return False, None


def title_matches_search(search_name, title):
    title_lower = title.lower()

    rules = {
        "ESP Horizon": ["esp", "horizon"],
        "ESP Viper": ["esp", "viper"],
        "ESP Mirage": ["esp", "mirage"],
        "ESP M-I": ["esp", "m-i"],
        "ESP M-II": ["esp", "m-ii"],
        "ESP Snapper": ["esp", "snapper"],
        "ESP Star": ["esp", "star"],
        "ESP Eclipse": ["esp", "eclipse"],
        "ESP Throbber": ["esp", "throbber"],

        "Jackson Kelly": ["jackson", "kelly"],
        "Jackson KE": ["jackson", "ke"],
        "Jackson RR": ["jackson", "rr"],
        "Jackson KV": ["jackson", "kv"],
        "Jackson Soloist": ["jackson", "soloist"],

        "Music Man Petrucci": ["music", "man"],
        "Music Man JP7": ["jp7"],
        "Music Man JP6": ["jp6"],
        "Music Man Luke": ["luke"],
        "Music Man Axis": ["axis"],
    }

    required_words = rules.get(search_name)
    if not required_words:
        return True

    return all(word in title_lower for word in required_words)


def extract_price(text):
    match = re.search(r"\$[\d,]+(?:\.\d{2})?", text)
    return match.group(0) if match else "Price not found"


def extract_listing_image(listing):
    try:
        image_url = listing.evaluate("""
            el => {
                const card = el.closest("li, article, div");
                if (!card) return null;

                const img = card.querySelector("img");
                if (!img) return null;

                return img.src || img.getAttribute("data-src") || img.getAttribute("src");
            }
        """)
        return image_url
    except Exception:
        return None

def get_listing_details(browser, link):
    details = {
        "price": "Price not found",
        "image_url": None
    }

    try:
        listing_page = browser.new_page()
        listing_page.goto(link, wait_until="domcontentloaded")
        listing_page.wait_for_timeout(3000)

        page_text = listing_page.locator("body").inner_text()
        details["price"] = extract_price(page_text)

        image_url = listing_page.evaluate("""
            () => {
                const ogImage = document.querySelector('meta[property="og:image"]');
                if (ogImage) return ogImage.content;

                const twitterImage = document.querySelector('meta[name="twitter:image"]');
                if (twitterImage) return twitterImage.content;

                return null;
            }
        """)

        details["image_url"] = image_url

        listing_page.close()

    except Exception as e:
        print("Could not get listing details:", e)

    return details

def send_discord_alert(webhook_url, search_name, title, price, link, image_url=None):
    embed = {
        "title": title[:250],
        "url": link,
        "description": "🔥 **NEW REVERB LISTING**",
        "fields": [
            {
                "name": "Search",
                "value": search_name,
                "inline": True
            },
            {
                "name": "Price",
                "value": price,
                "inline": True
            },
            {
                "name": "Source",
                "value": "Reverb",
                "inline": True
            }
        ],
        "color": 15158332
    }

    if image_url:
        embed["image"] = {"url": image_url}

    payload = {
        "content": "🔥 **NEW REVERB LISTING**",
        "embeds": [embed]
    }

    response = requests.post(webhook_url, json=payload)
    print("Discord status:", response.status_code)


def scrape_search(browser, page, search_name, search_url, seen_links, bad_keywords):
    print(f"\nChecking search: {search_name}")

    page.goto(search_url, wait_until="domcontentloaded")
    page.wait_for_timeout(5000)

    listings = page.locator("a[href*='/item/']")
    print("Listings found:", listings.count())

    new_count = 0

    for i in range(min(20, listings.count())):
        listing = listings.nth(i)

        title = listing.inner_text().strip()

        title = listing.inner_text().strip()

        try:
            card_text = listing.evaluate("""
                el => {
                    const card = el.closest("li, article, div");
                   return card ? card.innerText : el.innerText;
        }
    """)
        except Exception:
            card_text = title

        link = listing.get_attribute("href")

        if not link:
            continue

        link = clean_link(link)

        if link in seen_links:
            print("Already seen:", link)
            continue

        bad, keyword = is_bad_suggestion(title, bad_keywords)
        if bad:
            print(f"Skipped bad suggestion because of keyword '{keyword}': {title[:100]}")
            save_seen_link(link)
            seen_links.add(link)
            continue

        if not title_matches_search(search_name, title):
            print(f"Skipped because title does not match search: {title[:100]}")
            save_seen_link(link)
            seen_links.add(link)
            continue

        details = get_listing_details(browser, link)

        price = details["price"]
        image_url = None

        print("=" * 50)
        print("LISTING PAGE PRICE:", price)
        print("=" * 50)
        print("CARD TEXT:", card_text[:500])

        print("New listing:", title[:100])
        print("Price:", price)
        print("Image:", image_url)

        if is_lefty_listing(title):
            print("ROUTING: LOOK NOW")
            send_discord_alert(
                ALERT_WEBHOOK,
        search_name,
        title[:300],
        price,
        link,
        image_url
    )
else:
    print("ROUTING: POTENTIAL DEALS")
    send_discord_alert(
        POTENTIAL_WEBHOOK,
        search_name,
        title[:300],
        price,
        link,
        image_url
    )
        
        save_seen_link(link)
        seen_links.add(link)
        new_count += 1

    print(f"New alerts sent for {search_name}: {new_count}")
    return new_count


def main():
    seen_links = load_file_lines(SEEN_FILE)
    bad_keywords = load_file_lines(BAD_KEYWORDS_FILE)

    total_new = 0

    with sync_playwright() as p:
        browser = p.chromium.launch(headless=True)
        page = browser.new_page()

        for search_name, search_url in SEARCHES.items():
            total_new += scrape_search(browser, page, search_name, search_url, seen_links, bad_keywords)

        print("\nTotal new alerts sent:", total_new)

        input("Press Enter to close...")
        browser.close()


if __name__ == "__main__":
    main()