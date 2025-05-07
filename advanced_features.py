import dns.resolver
import tldextract
import re
from bs4 import BeautifulSoup
import requests
import ssl
import socket
from urllib.parse import urlparse
import whois
from datetime import datetime

class AdvancedFeatureExtraction:
    def __init__(self, url):
        self.url = url
        self.domain = urlparse(url).netloc
        self.tld_info = tldextract.extract(url)
        self.features = {}
        
    def extract_advanced_features(self):
        """Extract all advanced features"""
        self.features.update({
            'dns_features': self._get_dns_features(),
            'ssl_features': self._get_ssl_features(),
            'domain_features': self._get_domain_features(),
            'content_features': self._get_content_features()
        })
        return self.features
    
    def _get_dns_features(self):
        """Extract DNS-related features"""
        features = {}
        try:
            # Get DNS records
            domain = self.tld_info.registered_domain
            features['has_mx_record'] = bool(dns.resolver.resolve(domain, 'MX'))
            features['has_spf_record'] = bool(dns.resolver.resolve(domain, 'TXT'))
            features['nameserver_count'] = len(dns.resolver.resolve(domain, 'NS'))
            
            # Check for common DNS-based phishing indicators
            ip_addresses = dns.resolver.resolve(domain, 'A')
            features['multiple_ip_addresses'] = len(ip_addresses) > 1
            
        except Exception as e:
            features = {
                'has_mx_record': False,
                'has_spf_record': False,
                'nameserver_count': 0,
                'multiple_ip_addresses': False
            }
        return features
    
    def _get_ssl_features(self):
        """Extract SSL/TLS certificate features"""
        features = {}
        try:
            hostname = self.domain
            context = ssl.create_default_context()
            with socket.create_connection((hostname, 443)) as sock:
                with context.wrap_socket(sock, server_hostname=hostname) as ssock:
                    cert = ssock.getpeercert()
                    
                    features['ssl_valid'] = True
                    features['cert_issuer'] = cert['issuer'][0][0][1]
                    features['cert_expiry_days'] = (datetime.strptime(cert['notAfter'], 
                                                                    '%b %d %H:%M:%S %Y %Z') - 
                                                  datetime.now()).days
                    features['cert_version'] = cert['version']
        except:
            features = {
                'ssl_valid': False,
                'cert_issuer': None,
                'cert_expiry_days': -1,
                'cert_version': None
            }
        return features
    
    def _get_domain_features(self):
        """Extract domain-specific features"""
        features = {}
        try:
            # Domain age and registration info
            whois_info = whois.whois(self.domain)
            features['domain_age_days'] = (datetime.now() - whois_info.creation_date[0]).days
            features['domain_expiry_days'] = (whois_info.expiration_date[0] - datetime.now()).days
            features['domain_updated_days'] = (datetime.now() - whois_info.updated_date[0]).days
            
            # TLD analysis
            features['tld_type'] = self.tld_info.suffix
            features['subdomain_count'] = len(self.tld_info.subdomain.split('.')) if self.tld_info.subdomain else 0
            
        except:
            features = {
                'domain_age_days': -1,
                'domain_expiry_days': -1,
                'domain_updated_days': -1,
                'tld_type': None,
                'subdomain_count': -1
            }
        return features
    
    def _get_content_features(self):
        """Extract webpage content features"""
        features = {}
        try:
            response = requests.get(self.url, timeout=5)
            soup = BeautifulSoup(response.text, 'html.parser')
            
            # Form analysis
            forms = soup.find_all('form')
            features['form_count'] = len(forms)
            features['external_form_action'] = any(
                form.get('action', '').startswith(('http', 'https')) 
                for form in forms
            )
            
            # Link analysis
            links = soup.find_all('a')
            external_links = [link for link in links 
                            if link.get('href', '').startswith(('http', 'https'))]
            features['external_link_ratio'] = len(external_links) / len(links) if links else 0
            
            # Resource loading
            scripts = soup.find_all('script', src=True)
            features['external_js_ratio'] = len([s for s in scripts 
                                               if s['src'].startswith(('http', 'https'))]) / len(scripts) if scripts else 0
            
            # Meta information
            features['has_favicon'] = bool(soup.find('link', rel='icon'))
            features['has_description'] = bool(soup.find('meta', attrs={'name': 'description'}))
            
        except:
            features = {
                'form_count': -1,
                'external_form_action': False,
                'external_link_ratio': -1,
                'external_js_ratio': -1,
                'has_favicon': False,
                'has_description': False
            }
        return features
