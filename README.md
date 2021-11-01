### Phisher

#### How to create a website.
1. Copy the template to another webdirectory for your phishing domain and set paylods to have the appropriate permissions.
```
root@phishing~# cp /var/www/html/template /var/www/html/phishingdomain.com/
root@phishing~# chmod www-data:wwww-data /var/www/html/phishingdomain.com/payloads/
```
2. Create a phishingdomain.com.conf file for the phishing domain in /etc/apache2/site-avaliable/
```
root@phishing~# cat /etc/apache2/sites-available/phishingdomain.com.conf
<VirtualHost *:80>
	# The ServerName directive sets the request scheme, hostname and port that
	# the server uses to identify itself. This is used when creating
	# redirection URLs. In the context of virtual hosts, the ServerName
	# specifies what hostname must appear in the request's Host: header to
	# match this virtual host. For the default virtual host (this file) this
	# value is not decisive as it is used as a last resort host regardless.
	# However, you must set it for any further virtual host explicitly.
	ServerName phishingdomain.com

	ServerAdmin webmaster@localhost
	DocumentRoot /var/www/html/phishingdomain.com/

	# Available loglevels: trace8, ..., trace1, debug, info, notice, warn,
	# error, crit, alert, emerg.
	# It is also possible to configure the loglevel for particular
	# modules, e.g.
	#LogLevel info ssl:warn

	ErrorLog ${APACHE_LOG_DIR}/error.log
	CustomLog ${APACHE_LOG_DIR}/access.log combined

	# For most configuration files from conf-available/, which are
	# enabled or disabled at a global level, it is possible to
	# include a line for only one particular virtual host. For example the
	# following line enables the CGI configuration for this host only
	# after it has been globally disabled with "a2disconf".
	#Include conf-available/serve-cgi-bin.conf
	<FilesMatch "\.js$">
        	ForceType application/octet-stream
                Header set Content-Disposition attachment
	</FilesMatch>
</VirtualHost>
```
3. Enable the site with a2ensite.
```
root@phishing~# a2ensite phishingdomain.com.conf
```
4. Enable SSL for the site.
```
root@phishing~# certbot --apache -d phishingdomain.com
```
5. Create a phishing directory and fix the PHP files to point towards your phishing directory.
```
root@phishing~# mkdir /home/directory/phishing\ directory/
root@phishing:/var/www/html/payload-only-template# grep -r "\-\- phishing directory \-\-"
index.php:            $fd = fopen("-- phishing directory --/blocked.txt", "a");
index.php:        $fd = fopen("-- phishing directory --/visits.txt", "a");
download.php:        $fd = fopen("-- phishing directory --/downloads.txt", "a");
```
