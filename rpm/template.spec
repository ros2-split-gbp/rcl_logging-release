%bcond_without tests
%bcond_without weak_deps

%global __os_install_post %(echo '%{__os_install_post}' | sed -e 's!/usr/lib[^[:space:]]*/brp-python-bytecompile[[:space:]].*$!!g')
%global __provides_exclude_from ^/opt/ros/rolling/.*$
%global __requires_exclude_from ^/opt/ros/rolling/.*$

Name:           ros-rolling-rcl-logging-spdlog
Version:        2.5.1
Release:        1%{?dist}%{?release_suffix}
Summary:        ROS rcl_logging_spdlog package

License:        Apache License 2.0
Source0:        %{name}-%{version}.tar.gz

Requires:       %{name}-runtime%{?_isa?} = %{version}-%{release}
Requires:       ros-rolling-rcl-logging-interface-devel
Requires:       ros-rolling-rcpputils-devel
Requires:       ros-rolling-rcutils-devel
Provides:       %{name}-devel = %{version}-%{release}
Provides:       %{name}-doc = %{version}-%{release}
Provides:       ros-rolling-rcl-logging-packages(member)

%description
Implementation of rcl_logging API for an spdlog backend.

%package runtime
Summary:        Runtime-only files for rcl_logging_spdlog package
Requires:       ros-rolling-rcl-logging-interface-runtime
Requires:       ros-rolling-rcpputils-runtime
Requires:       ros-rolling-rcutils-runtime
Requires:       ros-rolling-spdlog-vendor-runtime
Requires:       spdlog-devel
Requires:       ros-rolling-ros-workspace-runtime
BuildRequires:  ros-rolling-ament-cmake-ros-devel
BuildRequires:  ros-rolling-rcl-logging-interface-devel
BuildRequires:  ros-rolling-rcpputils-devel
BuildRequires:  ros-rolling-rcutils-devel
BuildRequires:  ros-rolling-spdlog-vendor-devel
BuildRequires:  spdlog-devel
BuildRequires:  ros-rolling-ros-workspace-devel

%if 0%{?with_tests}
BuildRequires:  ros-rolling-ament-lint-auto-devel
BuildRequires:  ros-rolling-ament-lint-common-devel
BuildRequires:  ros-rolling-performance-test-fixture-devel
%endif

%if 0%{?with_weak_deps}
Supplements:    ros-rolling-rcl-logging-packages(all)
%endif

%description runtime
Runtime-only files for rcl_logging_spdlog package

%prep
%autosetup -p1

%build
# In case we're installing to a non-standard location, look for a setup.sh
# in the install tree and source it.  It will set things like
# CMAKE_PREFIX_PATH, PKG_CONFIG_PATH, and PYTHONPATH.
if [ -f "/opt/ros/rolling/setup.sh" ]; then . "/opt/ros/rolling/setup.sh"; fi
mkdir -p .obj-%{_target_platform} && cd .obj-%{_target_platform}
%cmake3 \
    -UINCLUDE_INSTALL_DIR \
    -ULIB_INSTALL_DIR \
    -USYSCONF_INSTALL_DIR \
    -USHARE_INSTALL_PREFIX \
    -ULIB_SUFFIX \
    -DCMAKE_INSTALL_PREFIX="/opt/ros/rolling" \
    -DAMENT_PREFIX_PATH="/opt/ros/rolling" \
    -DCMAKE_PREFIX_PATH="/opt/ros/rolling" \
    -DSETUPTOOLS_DEB_LAYOUT=OFF \
%if !0%{?with_tests}
    -DBUILD_TESTING=OFF \
%endif
    ..

%make_build

%install
# In case we're installing to a non-standard location, look for a setup.sh
# in the install tree and source it.  It will set things like
# CMAKE_PREFIX_PATH, PKG_CONFIG_PATH, and PYTHONPATH.
if [ -f "/opt/ros/rolling/setup.sh" ]; then . "/opt/ros/rolling/setup.sh"; fi
%make_install -C .obj-%{_target_platform}

for f in \
    /opt/ros/rolling/include/ \
    /opt/ros/rolling/share/ament_index/resource_index/packages/ \
    /opt/ros/rolling/share/rcl_logging_spdlog/cmake/ \
    /opt/ros/rolling/share/rcl_logging_spdlog/package.dsv \
    /opt/ros/rolling/share/rcl_logging_spdlog/package.xml \
; do
    if [ -e %{buildroot}$f ]; then echo $f; fi
done > devel_files

%if 0%{?with_tests}
%check
# Look for a Makefile target with a name indicating that it runs tests
TEST_TARGET=$(%__make -qp -C .obj-%{_target_platform} | sed "s/^\(test\|check\):.*/\\1/;t f;d;:f;q0")
if [ -n "$TEST_TARGET" ]; then
# In case we're installing to a non-standard location, look for a setup.sh
# in the install tree and source it.  It will set things like
# CMAKE_PREFIX_PATH, PKG_CONFIG_PATH, and PYTHONPATH.
if [ -f "/opt/ros/rolling/setup.sh" ]; then . "/opt/ros/rolling/setup.sh"; fi
CTEST_OUTPUT_ON_FAILURE=1 \
    %make_build -C .obj-%{_target_platform} $TEST_TARGET || echo "RPM TESTS FAILED"
else echo "RPM TESTS SKIPPED"; fi
%endif

%files -f devel_files

%files runtime
/opt/ros/rolling
%exclude /opt/ros/rolling/include/
%exclude /opt/ros/rolling/share/ament_index/resource_index/packages/
%exclude /opt/ros/rolling/share/rcl_logging_spdlog/cmake
%exclude /opt/ros/rolling/share/rcl_logging_spdlog/package.dsv
%exclude /opt/ros/rolling/share/rcl_logging_spdlog/package.xml

%changelog
* Tue Apr 11 2023 Chris Lalancette <clalancette@openrobotics.org> - 2.5.1-1
- Autogenerated by Bloom

* Tue Mar 21 2023 Chris Lalancette <clalancette@openrobotics.org> - 2.5.0-2
- Autogenerated by Bloom

