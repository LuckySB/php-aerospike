# spec file for php-aerospike
#
# Dirty patched from remi repo .spec files
# i am sorry
#

%if 0%{?scl:1}
%global sub_prefix %{scl_prefix}
%scl_package         php-aerospike
%endif

%global gh_commit  9776c7235a1a36021d9d356d0816a9f0c18a6aae
%global gh_short   %(c=%{gh_commit}; echo ${c:0:7})
%global gh_owner   aerospike
%global gh_project aerospike-client-php
%global gh_date    20161114
#global prever     RC1

%global pecl_name  aerospike
%global with_zts   1
#%global with_zts   0%{!?_without_zts:%{?__ztsphp:1}}
%if "%{php_version}" < "5.6"
%global ini_name   %{pecl_name}.ini
%else
%global ini_name   40-%{pecl_name}.ini
%endif
%global with_tests 0%{!?_without_tests:1}

Name:           %{?sub_prefix}php-%{pecl_name}
Version:        3.4.13
#%if 0%{?gh_date}
#Release:        0.1.%{gh_date}git%{gh_short}%{?dist}%{!?scl:%{!?nophptag:%(%{__php} -r 'echo ".".PHP_MAJOR_VERSION.".".PHP_MINOR_VERSION;')}}
#%else
Release:        2%{?dist}%{!?scl:%{!?nophptag:%(%{__php} -r 'echo ".".PHP_MAJOR_VERSION.".".PHP_MINOR_VERSION;')}}
#%endif

Summary:        Client extension for Aerospike

Group:          Development/Languages
License:        BSD
URL:            https://github.com/%{gh_owner}/%{gh_project}
Source0:        https://github.com/%{gh_owner}/%{gh_project}/archive/%{gh_commit}/%{pecl_name}-%{version}.tar.gz
##Source0:        https://github.com/%{gh_owner}/%{gh_project}/archive/%{gh_commit}/%{pecl_name}-%{version}-%{gh_short}.tar.gz

BuildRequires:  %{?scl_prefix}php-devel
BuildRequires:  %{?scl_prefix}php-pear

Requires:       lua
Requires:       %{?scl_prefix}php(zend-abi) = %{php_zend_api}
Requires:       %{?scl_prefix}php(api) = %{php_core_api}
%{?_sclreq:Requires: %{?scl_prefix}runtime%{?_sclreq}%{?_isa}}

%if "%{?scl_prefix}" != "%{?sub_prefix}"
Provides:       %{?scl_prefix}php-%{pecl_name}               = %{version}-%{release}
Provides:       %{?scl_prefix}php-%{pecl_name}%{?_isa}       = %{version}-%{release}
%endif

%if "%{?vendor}" == "Remi Collet" && 0%{!?scl:1}
# Other third party repo stuff
%if "%{php_version}" > "5.5"
Obsoletes:     php55u-%{pecl_name}      <= %{version}
Obsoletes:     php55u-pecl-%{pecl_name} <= %{version}
Obsoletes:     php55w-%{pecl_name}      <= %{version}
Obsoletes:     php55w-pecl-%{pecl_name} <= %{version}
%endif
%if "%{php_version}" > "5.6"
Obsoletes:     php56u-%{pecl_name}      <= %{version}
Obsoletes:     php56u-pecl-%{pecl_name} <= %{version}
Obsoletes:     php56w-%{pecl_name}      <= %{version}
Obsoletes:     php56w-pecl-%{pecl_name} <= %{version}
%endif
%if "%{php_version}" > "7.0"
Obsoletes:     php70u-%{pecl_name}      <= %{version}
Obsoletes:     php70u-pecl-%{pecl_name} <= %{version}
Obsoletes:     php70w-%{pecl_name}      <= %{version}
Obsoletes:     php70w-pecl-%{pecl_name} <= %{version}
%endif
%if "%{php_version}" > "7.1"
Obsoletes:     php71u-%{pecl_name}      <= %{version}
Obsoletes:     php71u-pecl-%{pecl_name} <= %{version}
Obsoletes:     php71w-%{pecl_name}      <= %{version}
Obsoletes:     php71w-pecl-%{pecl_name} <= %{version}
%endif
%endif

%if 0%{?fedora} < 20 && 0%{?rhel} < 7
# Filter private shared
%{?filter_provides_in: %filter_provides_in %{_libdir}/.*\.so$}
%{?filter_setup}
%endif


%description
aerospike is an extension for PHP 5.x and 7.x

Package built for PHP %(%{__php} -r 'echo PHP_MAJOR_VERSION.".".PHP_MINOR_VERSION;')%{?scl: as Software Collection (%{scl} by %{?scl_vendor}%{!?scl_vendor:rh})}.


%prep
%setup -q -c

cp -pr %{pecl_name}-%{version} %{pecl_name}-%{version}-ZTS
sed -i 's/phpize/zts-phpize/' ./%{pecl_name}-%{version}/src/aerospike/build.sh
sed -i 's/which php-config/which zts-php-config/' ./%{pecl_name}-%{version}/src/aerospike/build.sh

cat  << 'EOF' | tee %{ini_name}
; Enable %{pecl_name} extension module
extension=%{pecl_name}.so
aerospike.udf.lua_system_path=/usr/local/aerospike/lua
aerospike.udf.lua_user_path=/usr/local/aerospike/usr-lua
EOF


%build
dir=`pwd`
cd %{pecl_name}-%{version}/src/aerospike
echo "Build...."
./build.sh
echo "Done build...."

cd $dir
cd %{pecl_name}-%{version}-ZTS/src/aerospike
echo "Build ZTS...."
./build.sh
echo "Done build ZTS...."

%install

# install configuration
make -C %{pecl_name}-%{version}/src/aerospike  install INSTALL_ROOT=%{buildroot}
make -C %{pecl_name}-%{version}-ZTS/src/aerospike  install INSTALL_ROOT=%{buildroot}

install -Dpm 644 %{ini_name} %{buildroot}%{php_inidir}/%{ini_name}
install -Dpm 644 %{ini_name} %{buildroot}%{php_ztsinidir}/%{ini_name}

%files

%config(noreplace) %{php_inidir}/%{ini_name}
%config(noreplace) %{php_ztsinidir}/%{ini_name}
%{php_extdir}/%{pecl_name}.so
%{php_ztsextdir}/%{pecl_name}.so


%changelog
* Mon Nov 14 2016 Sergey Bondarev <s.bondarev@southbridge.ru> - 3.4.13
- Initial packaging of 3.4.13

