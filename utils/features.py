# utils/features.py

import re
from urllib.parse import urlparse

def extract_features(url):
    features = {}

    # 1. Using IP address
    features["UsingIP"] = -1 if re.match(r"^(http|https)://\d+\.\d+\.\d+\.\d+", url) else 1

    # 2. Long URL
    features["LongURL"] = -1 if len(url) < 54 else (0 if len(url) <= 75 else 1)

    # 3. Shortening Service
    shortening_services = r"bit\.ly|tinyurl\.com|goo\.gl|ow\.ly|t\.co"
    features["ShortURL"] = -1 if re.search(shortening_services, url) else 1

    # 4. @ Symbol
    features["Symbol@"] = -1 if "@" in url else 1

    # 5. Redirecting (//)
    features["Redirecting//"] = -1 if url.count("//") > 1 else 1

    # 6. Prefix/Suffix (-)
    features["PrefixSuffix-"] = -1 if "-" in urlparse(url).netloc else 1

    # 7. SubDomains
    domain = urlparse(url).netloc
    dots = domain.count('.')
    if dots == 1:
        features["SubDomains"] = 1
    elif dots == 2:
        features["SubDomains"] = 0
    else:
        features["SubDomains"] = -1

    # 8. HTTPS
    features["HTTPS"] = 1 if url.startswith("https") else -1

    # Add placeholders for remaining 22 features
    additional_features = [
        "DomainRegLen", "Favicon", "NonStdPort", "HTTPSDomainURL", "RequestURL", "AnchorURL",
        "LinksInScriptTags", "ServerFormHandler", "InfoEmail", "AbnormalURL", "WebsiteForwarding",
        "StatusBarCust", "DisableRightClick", "UsingPopupWindow", "IframeRedirection",
        "AgeofDomain", "DNSRecording", "WebsiteTraffic", "PageRank", "GoogleIndex",
        "LinksPointingToPage", "StatsReport"
    ]
    for feat in additional_features:
        features[feat] = 0  # default neutral placeholder

    return list(features.values())
