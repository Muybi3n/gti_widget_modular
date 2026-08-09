// NOTE: This project is for Proof of Concept (POC) purposes only. It is not intended for production use.

// --- Static Data ---
const urlIocs = [
    { id: "https://skyslope.com@securedatas.info/verification/verifyuridentityonline?email=info@isrreports.com", ingest: "30 Mins Ago", first: "5 Days Ago", last: "5 Days Ago" },
    { id: "http://tracking.mimeeting.net/tracking/botclick?msgid=f1QnWpG_gxeGDySH5dpYYQ2&c=1952454385774808418", ingest: "1 Hour Ago", first: "1 Hour Ago", last: "1 Hour Ago" },
    { id: "https://196.251.117.226:7117/gate/", ingest: "14 Hours Ago", first: "3 Hours Ago", last: "1 Day Ago" }
];

const fileIocs = [
    { id: "9432b623f19a6980256123fbc4c5c6f27be5fbfb8ea67ee577af6d651ebc3649", ingest: "2 Hours Ago", first: "13 Days Ago", last: "13 Days Ago" },
    { id: "1c783c253435b450cbd2eeb01830eca20d71145bd63c1cdbe655d88f4d65143d", ingest: "1 Hours Ago", first: "2 Day Ago", last: "2 Hours Ago" },
    { id: "72b5838dfa34b7d405d664c48e9b4aee72b4e10ac5f9f4cc124045dcd6d311a8", ingest: "1 Day Ago", first: "1 Month Ago", last: "1 Month Ago" }
];

const vulnerabilityIocs = [
    { 
        cve: "CVE-2025-31324",
        updated: "6 days ago",
        published: "2025-04-22",
        mve: "MVE-2025-10681",
        description: "An Improper Authorization vulnerability exists that, when exploited, allows a remote attacker to execute arbitrary code.",
        risk: "CRITICAL",
        exploitState: "Confirmed",
        inWild: true,
        iocs: 12
    },
    { 
        cve: "CVE-2024-1709",
        updated: "8 days ago",
        published: "2024-02-19",
        mve: "MVE-2024-2354",
        description: "An Authentication Bypass vulnerability exists that, when exploited, allows a remote attacker to obtain unauthorized access.",
        risk: "CRITICAL",
        exploitState: "Wide",
        inWild: true,
        iocs: 8
    },
    { 
        cve: "CVE-2023-46805",
        updated: "8 days ago",
        published: "2024-01-10",
        mve: "MVE-2023-25396",
        description: "A Path Traversal vulnerability exists that, when exploited, allows a remote attacker to obtain unauthorized access.",
        risk: "CRITICAL",
        exploitState: "Wide",
        inWild: true,
        iocs: 11
    }
];
