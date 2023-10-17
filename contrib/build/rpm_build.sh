
TARBALL_NAME=vkbot
RELEASE="stable"

mkdir -p SOURCES
#git archive --format tar --output SOURCES/${TARBALL_NAME}.tar HEAD
tar -czvf SOURCES/${TARBALL_NAME}.tar *
yum-builddep -y -q contrib/build/vkbot-c7x64.spec

python3.11 -m pip install virtualenv

QA_SKIP_BUILD_ROOT=1 rpmbuild -bb \
      --clean \
      --define "_topdir `pwd`" \
      --define "_tarballname ${TARBALL_NAME}" \
      --define "_name $(python3.11 setup.py --name)" \
      --define "_version $(python3.11 setup.py --version)" \
      --define "_release ${RELEASE}" \
      contrib/build/vkbot-c7x64.spec \
