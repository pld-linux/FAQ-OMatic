# TODO: webapp config
%include	/usr/lib/rpm/macros.perl
Summary:	Faq-O-Matic - a CGI-based system that automates the process of maintaining a FAQ
Summary(pl.UTF-8):	Faq-O-Matic - oparty o CGI system automatyzujący proces utrzymywania FAQ
Name:		FAQ-OMatic
Version:	2.721
Release:	2
License:	GPL
Group:		Applications/WWW
Source0:	http://dl.sourceforge.net/faqomatic/%{name}-%{version}.tar.gz
# Source0-md5:	44a0b0fbe58d07ee3b54c21434829514
Patch0:		faqomatic-tmp-pass.patch
URL:		http://faqomatic.sourceforge.net/
BuildRequires:	rpm-perlprov >= 4.1-13
Requires:	webserver = apache
Requires:	rcs
Obsoletes:	perl-FAQ-OMatic
BuildArch:	noarch
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

%define         appdir		/home/services/httpd/cgi-bin
# TODO (after providing webapp config)
#define         appdir		/var/lib/%{name}

%description
The Faq-O-Matic is a CGI-based system that automates the process of
maintaining a FAQ (or Frequently Asked Questions list). It allows
visitors to your FAQ to take part in keeping it up-to-date. A
permission system also makes it useful as a help-desk application,
bug-tracking database, or documentation system.

%description -l pl.UTF-8
Faq-O-Matic to oparty o CGI system automatyzujący proces utrzymywania
FAQ (Frequently Asked Questions - listy najczęściej zadawanych pytań).
Pozwala gościom FAQ pomagać w uaktualnianiu go. Ma system uprawnień,
dzięki czemu jest przydatny także jako aplikacja helpdeskowa, baza
danych do śledzenia błędów lub system dokumentacji.

%prep
%setup -q
%patch0 -p1

%build
%{__perl} Makefile.PL \
	INSTALLDIRS=vendor

%{__make}

sed -i -e 's,/usr/local/share/perl5,%{perl_vendorlib},' fom

%install
rm -rf $RPM_BUILD_ROOT
install -d $RPM_BUILD_ROOT%{appdir}/fom-meta

%{__make} pure_install \
	DESTDIR=$RPM_BUILD_ROOT

install fom $RPM_BUILD_ROOT%{appdir}

%clean
rm -rf $RPM_BUILD_ROOT

%post
echo "Use password from %{_docdir}/%{name}-%{version}/fom_pass.txt.gz to activate your FAQ-OMatic."
echo "I.e.: gzip -cd %{_docdir}/%{name}-%{version}/fom_pass.txt.gz or sth like that."

%files
%defattr(644,root,root,755)
%doc Changes LICENSE README fom_pass.txt
%attr(755,root,root) %{appdir}/fom
%attr(775,root,http) %dir %{appdir}/fom-meta
%dir %{perl_vendorlib}/FAQ
%{perl_vendorlib}/FAQ/*.pm
%dir %{perl_vendorlib}/FAQ/OMatic
%{perl_vendorlib}/FAQ/OMatic/*.pm
%{_mandir}/man3/*
