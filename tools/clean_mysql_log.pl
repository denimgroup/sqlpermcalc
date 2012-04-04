#!/usr/bin/perl

# Copyright (c) 2012 Denim Group, Ltd.
# All rights reserved worldwide
# http://www.denimgroup.com/

open SQLLOG, "mysqlwatch.log" or die $!;
my @lines = <SQLLOG>;
close SQLLOG;

open SQLOUT, ">mysqlwatch.sql" or die $!;

# First 3 lines are not useful so skip them
# It makes life easier if we start at 2 and auto-skip the third
# on the first loop iteration start
$i = 2;

while($i < scalar(@lines)) {
        $i = $i + 1;
        $_ = $lines[$i];
        chop;
        @current_tokens = split;

        debug($i, "Full line is '$_'");
        if(($current_tokens[0] != 329) && ($current_tokens[2] != 329)) {
                debug($i, "Not a 329 Query line. Moving on");
                next;
        } else {
                debug($i, "Is a 329 Query line. Parsing for query");
        }

        $query_line = substr($_, index($_, "329 Query") + 10);
        debug($i, "First query line: '$query_line'");

        $save_i = $i;

        # Look ahead to see if the query continues
        while(!is_main_entry_line($save_i, $lines[$i + 1]) && $i <= scalar(@lines)) {
                debug($save_i, "Going to append the next line to the query");
                $line_to_append = $lines[$i + 1];
                chop($line_to_append);
                debug($save_i, "Next line being added: '$line_to_append;");
                $query_line .= " $line_to_append";
                debug($save_i, "Query so far is: '$query_line'");
                $i = $i + 1;
        }

        debug($save_i, "Total query: '$query_line'");
        print SQLOUT "$query_line\n";
}

close SQLOUT;

sub is_main_entry_line() {
        $base_line_num = $_[0];
        $orig_line = $_[1];
        chop($orig_line);
        $orig_line = ltrim($orig_line);
        debug($base_line_num, "is_main_entry_line: Line to check is '$orig_line'");

        @the_tokens = split(/[ \t]+/, $orig_line);
        $new_line = join(',', @the_tokens);
        debug($base_line_num, "is_main_entry_line: Tokens are: '$new_line'");
        if($the_tokens[0] =~ /^\d+/ || $the_tokens[2] =~ /^\d+/) {
                debug($base_line_num, "is_main_entry_line: Return will be true");
                $ret_val = 1;
        } else {
                debug($base_line_num, "is_main_entry_line: Return will be false");
                $ret_val = 0;
        }

        return $ret_val;
}

sub debug() {
        $line = $_[0] + 1;
        $message = $_[1];

        print "Line $line: $message\n";
}

# Left trim function to remove leading whitespace
sub ltrim($)
{
        my $string = shift;
        $string =~ s/^\s+//;
        return $string;
}

