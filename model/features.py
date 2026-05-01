import re, tldextract
from urllib.parse import urlparse

def extract_features(url):
    parsed = urlparse(url)
    ext    = tldextract.extract(url)
    domain = ext.domain
    sub    = ext.subdomain

    return [
        # ── Original 20 ──────────────────────────────────────
        len(url),                                               # 1.  URL total length
        url.count('.'),                                         # 2.  dot count
        url.count('-'),                                         # 3.  hyphen count
        url.count('@'),                                         # 4.  @ symbol
        url.count('/'),                                         # 5.  slash count
        url.count('?'),                                         # 6.  query params
        url.count('='),                                         # 7.  equals signs
        url.count('%'),                                         # 8.  percent encoding
        1 if parsed.scheme == 'https' else 0,                  # 9.  HTTPS?
        1 if re.match(r'\d+\.\d+\.\d+\.\d+',
                      parsed.netloc) else 0,                   # 10. IP address used?
        len(sub.split('.')) if sub else 0,                     # 11. subdomain depth
        len(domain),                                            # 12. domain name length
        len(parsed.path),                                       # 13. URL path length
        len(parsed.query),                                      # 14. query string length
        1 if 'login'   in url.lower() else 0,                  # 15. "login" keyword
        1 if 'secure'  in url.lower() else 0,                  # 16. "secure" keyword
        1 if 'bank'    in url.lower() else 0,                  # 17. "bank" keyword
        1 if 'account' in url.lower() else 0,                  # 18. "account" keyword
        1 if 'verify'  in url.lower() else 0,                  # 19. "verify" keyword
        len(ext.suffix),                                        # 20. TLD length

        # ── New 10 ───────────────────────────────────────────
        url.count('_'),                                         # 21. underscore count
        url.count('~'),                                         # 22. tilde count
        len(parsed.netloc),                                     # 23. hostname length
        1 if re.search(r'\d', domain) else 0,                  # 24. digits in domain?
        sum(c.isdigit() for c in url),                         # 25. total digit count
        1 if 'paypal'  in url.lower() else 0,                  # 26. "paypal" keyword
        1 if 'update'  in url.lower() else 0,                  # 27. "update" keyword
        1 if 'confirm' in url.lower() else 0,                  # 28. "confirm" keyword
        1 if 'signin'  in url.lower() else 0,                  # 29. "signin" keyword
        url.count('#'),                                         # 30. fragment count
    ]