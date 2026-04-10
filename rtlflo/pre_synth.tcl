# namespace eval ::tclapp::daxzio::version {
#   variable rev 0
# }

set versionfile "../../../version.txt"
set interimfile "../../../interim.txt"
file delete -force ${interimfile}

set now [clock seconds]
set timestr [clock format $now -format "%y%m%d"]
#set timestr "250319"
puts $timestr

if {[catch {open ${versionfile} "r"} fp error_message]} {
    set previous_version ""
    set rev 0
} else {
    set previous_version [gets $fp]
    close $fp
    if {[string first $timestr $previous_version] == 0} {
        set hex [string range $previous_version end-1 end]
        set rev [expr 0x$hex]
    } else {
        set rev 0
    }
}

puts "Previous Rev $previous_version"
for {set i $rev} {$i < 100} {incr i} {
    set rev_new [format %02x $i]
    set version "${timestr}${rev_new}"
    if {$previous_version != $version} {
        break
    }
}

set outfile [open ${interimfile} w]
puts $outfile "$version"
close $outfile

set GENERICS [get_property generic [current_fileset]]
# puts ${GENERICS}
regsub {G_FPGA_VERSION=32'h\d+} ${GENERICS} "G_FPGA_VERSION=32'h${version}" GENERICS2
# puts ${GENERICS2}
set_property generic ${GENERICS2} [current_fileset]

set GENERICS [get_property generic [current_fileset]]
puts ${GENERICS}
puts "Setting Version to: $version"
# set_property FPGA_VERSION $version [get_designs top]
# set env(FPGA_VERSION) $version

# set ::tclapp::daxzio::version::rev $version
# puts "Setting Version to tclapp: $::tclapp::daxzio::version::rev"
