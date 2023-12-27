import requests
import xml.etree.ElementTree as ET

def crawl_sitemap(url):
    response = requests.get(url)
    if response.status_code == 200:
        return response.text
    else:
        print(f"Failed to fetch sitemap. Status code: {response.status_code}")
        return None

def find_cass_resources(xml_content):
    cass_resources = []

    if xml_content:
        root = ET.fromstring(xml_content)
        namespace = {'sitemap': 'http://www.sitemaps.org/schemas/sitemap/0.9'}

        for url_element in root.findall('.//sitemap:url', namespaces=namespace):
            loc_element = url_element.find('sitemap:loc', namespaces=namespace)
            if loc_element is not None:
                url = loc_element.text
                if 'cass' in url:
                    cass_resources.append(url)

    return cass_resources

def main():
    sitemap_url = 'https://www.fca.org.uk/sitemap.xml?page=1'
    xml_content = crawl_sitemap(sitemap_url)

    if xml_content:
        cass_resources = find_cass_resources(xml_content)

        if cass_resources:
            print("CASS Resources:")
            for resource in cass_resources:
                print(resource)
        else:
            print("No CASS resources found in the sitemap.")
    else:
        print("Exiting due to failure in fetching sitemap.")

if __name__ == "__main__":
    main()
