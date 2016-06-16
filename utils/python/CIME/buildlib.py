"""
common utilities for buildlib
"""

from CIME.XML.standard_module_setup import *
from CIME.utils import expect, run_cmd, handle_standard_logging_options, setup_standard_logging_options
from CIME.case  import Case
import sys, os, argparse

logger = logging.getLogger(__name__)

###############################################################################
def parse_input(argv):
###############################################################################

    if "--test" in argv:
        test_results = doctest.testmod(verbose=True)
        sys.exit(1 if test_results.failed > 0 else 0)

    parser = argparse.ArgumentParser()

    setup_standard_logging_options(parser)

    parser.add_argument("caseroot", default=os.getcwd(),
                        help="Case directory")

    parser.add_argument("bldroot",
                        help="root for building library")

    parser.add_argument("libroot",
                        help="root for creating the library")

    args = parser.parse_args()

    handle_standard_logging_options(args)

    return args.caseroot, args.libroot, args.bldroot

###############################################################################
def build_data_lib(argv, compclass):
###############################################################################

    caseroot, libroot, bldroot = parse_input(argv)

    case = Case(caseroot)

    cimeroot  = case.get_value("CIMEROOT")

    # Write directory list (Filepath)
    compname = "d" + compclass
    with open('Filepath', 'w') as out:
        out.write(os.path.join(caseroot, "SourceMods", "src.%s" %compname) + "\n")
        out.write(os.path.join(cimeroot, "components", "data_comps", compname) + "\n")

    # Build the component
    run_gmake(case, compclass, libroot)

###############################################################################
def build_xcpl_lib(argv, compclass):
###############################################################################

    caseroot, libroot, bldroot = parse_input(argv)

    case = Case(caseroot)

    cimeroot  = case.get_value("CIMEROOT")

    # Write directory list
    compname = "x" + compclass
    with open('Filepath', 'w') as out:
        out.write(os.path.join(caseroot, "SourceMods", "src.%s", compname) + "\n")
        out.write(os.path.join(cimeroot, "components", "xcpl_comps", "xshare") + "\n")
        out.write(os.path.join(cimeroot, "components", "xcpl_comps",compname, "cpl") + "\n")

    # Build the component
    run_gmake(case, compclass, libroot)

###############################################################################
def build_stub_lib(argv, compclass):
###############################################################################

    caseroot, libroot, bldroot = parse_input(argv)

    case = Case(caseroot)

    cimeroot = case.get_value("CIMEROOT")

    # Write directory list
    compname = "s" + compclass
    with open('Filepath', 'w') as out:
        out.write(os.path.join(caseroot, "SourceMods", "src.%s", compname) + "\n")
        out.write(os.path.join(cimeroot, "components", "stub_comps", "xshare") + "\n")
        out.write(os.path.join(cimeroot, "components", "stub_comps",compname, "cpl") + "\n")

    # Build the component
    run_gmake(case, compclass, libroot)

###############################################################################
def run_gmake(case, compclass, libroot, libname="", user_cppdefs=""):
###############################################################################

    caseroot  = case.get_value("CASEROOT")
    casetools = case.get_value("CASETOOLS")
    gmake_j   = case.get_value("GMAKE_J")
    gmake     = case.get_value("GMAKE")
    mach      = case.get_value("MACH")

    complib = ""
    if libname:
        complib  = os.path.join(libroot, "lib%s.a" % libname)
    else:
        complib  = os.path.join(libroot, "lib%s.a" % compclass)

    makefile = os.path.join(casetools, "Makefile")
    macfile  = os.path.join(caseroot, "Macros.%s" % mach)

    if user_cppdefs:
        cmd = "%s complib -j %d MODEL=%s COMPLIB=%s -f %s MACFILE=%s USER_CPPDEFS=%s" \
            % (gmake, gmake_j, compclass, complib, makefile, macfile, user_cppdefs )
    else:
        cmd = "%s complib -j %d MODEL=%s COMPLIB=%s -f %s MACFILE=%s " \
            % (gmake, gmake_j, compclass, complib, makefile, macfile )

    rc, out, err = run_cmd(cmd, ok_to_fail=True)
    expect(rc == 0, "Command %s failed rc=%d\nout=%s\nerr=%s" % (cmd, rc, out, err))

    logger.info("Command %s completed with output %s\nerr %s" ,cmd, out, err)
