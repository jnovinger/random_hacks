<?php

/**
 * A quick script to mess with my kids. Why? Because I have cool kids and it is
 * just plain fun.
 *
 * This script logs in to a specified GMail account and looks for any messages
 * present with the 'SAY' label.  I set up a GMail filter to grab any emails from
 * my phone with the word 'say' in it, archive them, and apply the 'SAY' label to
 * them. The script grabs the email body, constructs a SSH command that passes the
 * 'say' command to the Mac Mini in the living room.
 * 
 * Yes, this is definitely open to terminal injection, which is why I limit it to 
 * only my phone number.
 *
 * Dependencies:
 *  - a GMail account
 *  - a cellular phone capable of sending SMS messages to email addresses
 *  - a machine with PHP, compiled with the PHP-IMAP extension (or just apt-get install php5-imap !)
 *      (tangent: this appears to be a PITA on a Mac, so I did it on my Ubuntu 
 *      desktop machine and ran the 'say' command via SSH. Can you say lazy?)
 *  - a Mac somewhere on your local network that will scare the bejesus out of your kids
 *  - a key based SSH auth on the remote Mac (http://www.debian-administration.org/articles/530 for a quick howto)
 *  - for extra fun, throw it in your ~/bin folder and call it every now and then from cron
 *
 * @author Jason Novinger
 * @version 0.1
 * 
 */

/* gmail settings, would work with any IMAP provider
 * Notice the 'SAY' at the end of the $server assignment.  This is the Gmail 
 * Label that these message will be in, modify accordingly.
 */
$server = '{imap.gmail.com:993/ssl/novalidate-cert}SAY';
$username = 'account@gmail.com';                            // fill in with your GMail username
$password = 'password';                                     // fill in with your GMail password

/* local settings */
$mac = '192.168.1.xxx';                                     // fill in IP address of the remote Mac to run 'say' on
$mac_user = 'user';                                         // fill in username on the remote Mac
$phone = '7105551212';                                      // fill in phone number text sent from

/* connect */
$inbox = imap_open($server, $username, $password) or die('Cannot connect to Gmail: ' . imap_last_error() . "\n");

/* constuct search query */
$search = 'ALL FROM "'.$phone.'" UNSEEN';

/* grab emails in the label 'say' */
$lines = imap_search($inbox, $search);

/* loop through emails and store commands */
if($lines) {
    $commands = array();
    foreach ($lines as $line) {
        $body = strtolower(rtrim(imap_fetchbody($inbox, $line, 1)));
        $commands[] = 'ssh ' . $mac_user . '@' . $mac . ' "' . $body . '"';
    }
}

/* close connection as soon as possible */
imap_close($inbox);

/* run the commands on the remote mac to say the lines */
if (isset($commands)) {
    foreach($commands as $command) {
        exec($command);
        sleep(1);
    }
}

?>
