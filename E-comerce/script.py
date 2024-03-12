import requests
from urllib.parse import urlparse

def check_website(url):
    try:
        response = requests.get(url)
        response.raise_for_status()

        # Security checks (logic remains the same)
        parsed_url = urlparse(url)
        if parsed_url.scheme == 'https':
            if response.headers.get('Strict-Transport-Security'):
                result = "This website has a valid SSL certificate."
            else:
                result = "This website does not have a valid SSL certificate."
        else:
            result = "This website is not using HTTPS, which could be a security concern."

        security_headers = response.headers
        results = [result]  # Store results in a list

        if 'X-Content-Type-Options' in security_headers:
            results.append("X-Content-Type-Options header is present.")
        else:
            results.append("Warning: X-Content-Type-Options header is missing. This could expose the website to MIME-sniffing attacks.")

        if 'X-Frame-Options' in security_headers:
            results.append("X-Frame-Options header is present.")
        else:
            results.append("Warning: X-Frame-Options header is missing. This could expose the website to clickjacking attacks.")

        if 'Content-Security-Policy' in security_headers:
            results.append("Content-Security-Policy header is present.")
        else:
            results.append("Warning: Content-Security-Policy header is missing. This could expose the website to various client-side attacks.")

        if 'X-XSS-Protection' in security_headers:
            results.append("X-XSS-Protection header is present.")
        else:
            results.append("Warning: X-XSS-Protection header is missing. This could expose the website to cross-site scripting (XSS) attacks.")

        return results  # Return the list of results

    except requests.RequestException as e:
        return ["Error:", str(e)]  # Return an error message list

# Example usage (assuming called from script.py)
def main():
    url = input("Enter the website URL to check: ")
    results = check_website(url)
    print("\n".join(results))  # Print results on the server-side console

if __name__ == "__main__":
    main()