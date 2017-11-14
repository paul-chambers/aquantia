%define destdir /lib/modules/%(uname -r)/kernel/drivers/atlantic

Summary: AQtion(R) Ethernet driver
Name: Aquantia-AQtion
Vendor: aQuantia Corporation
Version: 1.6.7
Release: 1
License: GPLv2
Group: System Environment/Kernel
Provides: %{name}
URL:   http://www.aquantia.com/
BuildRoot: %{_tmppath}/%{name}-%{version}-root

#list of sources
Source0:  Aquantia-AQtion-%{version}.tar.gz

%description
This package contains aQuantia AQtion Ethernet Linux driver

%pre
if [ $(uname -r) != "%(uname -r)" ]; then
echo "Kernel %(uname -r) not supported by this RPM."
exit 1
fi

%prep
%setup -q

%build
make clean
make

%install
mkdir -p %{destdir}
mkdir -p %{buildroot}%{destdir}

ls %{destdir} > /dev/null 2> /dev/null
if [ $? != 0 ]; then
echo "%{destdir} is not here. Unable to install the driver."
exit 1
fi
install -m 755 atlantic.ko %{buildroot}%{destdir}/atlantic.ko
install -m 755 netif.sh %{buildroot}%{destdir}/netif.sh

%clean
rm -rf %{buildroot}

%post
/sbin/depmod -a
/sbin/modprobe atlantic
/sbin/udevadm settle
sh %{destdir}/netif.sh

%postun
/sbin/rmmod atlantic

%files
%defattr(-,root,root)
%{destdir}/atlantic.ko
%{destdir}/netif.sh

%changelog
* Fri May 05 2017 aQuantia
-Release v1.06.07.0

