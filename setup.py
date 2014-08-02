from distutils.core import setup
import py2exe
setup(
	name="Adobe Creator",
	description="Software para la limpieza de accesos directos no usados",
	author="RyS ltda",
	author_email="manhero@outlook.es",
	license="gpl",
	# scripts=["dir.pyw"],
	windows=["ccfk.py"],
	options={"py2exe":{"bundle_files": 1}},
	zipfile=None
)