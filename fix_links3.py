#!/usr/bin/env python3
"""Third-pass: manual mapping for remaining unmatched links."""

import re
import glob

CONTENT_DIR = "src/content/questions"

# Manual title → slug overrides for wording mismatches
MANUAL_MAP = {
    "Can a Voluntary Disclosure Agreement protect me from penalties?": "can-a-vda-protect-me-from-penalties",
    "Do Amazon FBA or marketplace sales count toward my economic nexus threshold?": "do-marketplace-sales-count-toward-my-nexus-threshold",
    "Do Amazon and Etsy sales count toward my nexus threshold?": "do-amazon-etsy-sales-count-toward-nexus-threshold",
    "Do Amazon marketplace sales count toward my economic nexus threshold?": "do-marketplace-sales-count-toward-my-nexus-threshold",
    "Do I need to collect sales tax in every state?": "what-is-economic-nexus",
    "Does Amazon collecting sales tax affect my nexus threshold calculations?": "do-marketplace-sales-count-toward-my-nexus-threshold",
    "Does Amazon collecting sales tax mean I don't need to register?": "if-amazon-collects-sales-tax-do-i-still-need-to-register",
    "Does Amazon's 1099-K alert states to my sales tax exposure?": "does-amazon-1099k-alert-states-to-sales-tax-exposure",
    "Does Amazon's 1099-K data alert states to my sales tax exposure?": "does-amazon-1099k-alert-states-to-sales-tax-exposure",
    "Does having a remote employee in another state create nexus?": "does-remote-employee-create-sales-tax-nexus",
    "How do I file sales tax returns across 20+ states?": "how-do-i-file-across-20-plus-states",
    "How do I find which states Amazon stores my FBA inventory?": "how-to-find-which-states-amazon-stores-fba-inventory",
    "How do I handle nexus created by a 3PL I just started using?": "how-to-handle-nexus-created-by-3pl",
    "How do I handle sales tax when I sell on Amazon AND my own Shopify store?": "how-do-i-handle-sales-tax-selling-amazon-and-shopify",
    "How do I handle sales tax when I sell on a marketplace AND my own store?": "how-do-i-handle-sales-tax-selling-amazon-and-shopify",
    "How do I handle sales tax when selling on Amazon and Shopify?": "how-do-i-handle-sales-tax-selling-amazon-and-shopify",
    "How do I handle sales tax when selling on both Amazon and Shopify?": "how-do-i-handle-sales-tax-selling-amazon-and-shopify",
    "How do I manage FBA nexus when Amazon moves inventory between states without telling me?": "how-to-manage-fba-nexus-when-amazon-moves-inventory",
    "How do I manage FBA nexus when Amazon moves inventory between states?": "how-to-manage-fba-nexus-when-amazon-moves-inventory",
    "How do I manage FBA nexus when Amazon moves inventory without my control?": "how-to-manage-fba-nexus-when-amazon-moves-inventory",
    "How do I manage FBA nexus when Amazon moves inventory?": "how-to-manage-fba-nexus-when-amazon-moves-inventory",
    "How do I manage sales tax compliance across 30+ states?": "how-do-i-manage-compliance-across-30-to-45-states",
    "How do I reconcile Amazon 1099-K data with my sales tax filings?": "how-do-i-reconcile-amazon-1099k-data-with-my-sales-tax-filings",
    "How do I set the correct product tax code in Shopify?": "how-do-i-set-correct-product-tax-code-in-shopify",
    "How does selling on Amazon affect my sales tax obligations?": "if-amazon-collects-sales-tax-do-i-still-need-to-register",
    "If Amazon already collects sales tax for me, do I still need to register?": "if-amazon-collects-sales-tax-do-i-still-need-to-register",
    "If Amazon already collects sales tax, do I still need to register in those states?": "if-amazon-collects-sales-tax-do-i-still-need-to-register",
    "If Amazon already collects sales tax, do I still need to register?": "if-amazon-collects-sales-tax-do-i-still-need-to-register",
    "If Amazon already collects, do I still need to register in those states?": "if-amazon-collects-sales-tax-do-i-still-need-to-register",
    "Is Shopify's built-in tax enough for multi-state compliance?": "is-shopify-built-in-tax-enough-for-multi-state-compliance",
    "What are the economic nexus thresholds for all 50 states?": "economic-nexus-thresholds-by-state",
    "What data do I need to export from Avalara before leaving?": "what-data-do-i-need-to-export-from-avalara",
    "What data do I need to export from TaxJar before leaving?": "what-data-do-i-need-to-export-from-taxjar",
    "What do I do the moment I cross an economic nexus threshold?": "what-to-do-when-you-cross-economic-nexus-threshold",
    "What is a VDA, and when should I use one?": "what-is-a-voluntary-disclosure-agreement",
    "What is the SST program and is it worth using?": "what-is-the-streamlined-sales-tax-sst-program",
    "What is the Streamlined Sales Tax (SST) Program and is it worth using?": "what-is-the-streamlined-sales-tax-sst-program",
    "What is the difference between SST states and non-SST states?": "what-is-the-difference-between-sst-and-non-sst-states",
    "What is the difference between US sales tax, EU VAT, and Canadian GST/HST?": "what-is-the-difference-between-us-sales-tax-eu-vat-and-canadian-gst",
    "What is the difference between physical nexus and economic nexus?": "what-is-economic-nexus",
    "What is the risk of assuming your marketplace is handling all your tax?": "what-is-the-risk-of-assuming-marketplace-handles-all-tax",
    "What questions should I ask a new provider before committing?": "what-questions-should-i-ask-a-new-sales-tax-provider",
    "What states have no sales tax?": "which-states-have-no-sales-tax",
    "What was South Dakota v. Wayfair?": "what-is-the-wayfair-ruling",
    "Who is liable in an audit if my exemption certificate is invalid?": "what-happens-if-i-accept-an-invalid-exemption-certificate",
    "Sales tax in California, complete guide": "sales-tax-in-california",
    "Sales tax in California": "sales-tax-in-california",
    "Sales tax in Colorado": "sales-tax-in-colorado",
    "Sales tax in Louisiana": "sales-tax-in-louisiana",
    "Sales tax in Texas": "sales-tax-in-texas",
    "Sales tax in Washington": "sales-tax-in-washington",
    "Sales tax software vs. managed compliance service: which is right for me?": "sales-tax-software-vs-managed-compliance-service",
    "Is switching sales tax software worth it?": "is-switching-sales-tax-software-worth-it",
    "Is switching sales tax software worth the disruption?": "is-switching-sales-tax-software-worth-it",
    "How do I switch from Avalara to a different provider?": "what-is-the-avalara-separation-process",
    "How do I switch from TaxJar to a different provider?": "how-do-i-switch-from-taxjar",
    "How do I switch from TaxJar?": "how-do-i-switch-from-taxjar",
    "Economic nexus thresholds by state": "economic-nexus-thresholds-by-state",
    "Economic nexus thresholds by state, how do they vary?": "economic-nexus-thresholds-by-state",
    "What are the sales tax filing deadlines by state?": "sales-tax-filing-deadlines-by-state",
    "How do I integrate TaxCloud with Shopify?": "how-do-i-integrate-taxcloud-with-shopify-bigcommerce-woocommerce",
    "Should I outsource sales tax compliance or build in-house?": "should-i-outsource-sales-tax-compliance-or-build-in-house",
    "Can a compliance platform handle B2B and DTC simultaneously?": "can-a-compliance-platform-handle-b2b-and-dtc-simultaneously",
    "Colorado home rule cities, what they are and how they affect filing": "colorado-home-rule-cities-what-they-are-and-how-they-affect-filing",
    "What R&D and manufacturing exemptions exist?": "what-rd-and-manufacturing-exemptions-exist",
    "How do I close a sales tax permit?": "how-do-i-close-a-sales-tax-permit",
    "How do I collect and store exemption certificates?": "how-do-i-collect-and-store-exemption-certificates",
    "How do I file a final return when closing a permit?": "how-do-i-file-a-final-return-when-closing-a-permit",
    "How do I file across 20+ states?": "how-do-i-file-across-20-plus-states",
    "How do I file an amended sales tax return?": "how-do-i-file-an-amended-sales-tax-return",
    "How do I handle VAT for EU customers?": "how-do-i-handle-vat-for-eu-customers",
    "How do I handle VAT for EU customers as a US-based ecommerce brand?": "how-do-i-handle-vat-for-eu-customers",
    "How do I handle sales tax on refunds when filing?": "how-do-i-handle-sales-tax-on-refunds-when-filing",
    "How do I manage compliance across 30–45 states?": "how-do-i-manage-compliance-across-30-to-45-states",
    "How do I manage sales tax for a WooCommerce store?": "how-do-i-manage-sales-tax-for-a-woocommerce-store",
    "How do I prioritize states if I have retroactive exposure in multiple places?": "how-do-i-prioritize-which-states-to-address-first",
    "How do I prioritize which states to address first?": "how-do-i-prioritize-which-states-to-address-first",
    "How do I reconcile my Amazon 1099-K with my sales tax filings?": "how-do-i-reconcile-amazon-1099k-data-with-my-sales-tax-filings",
    "How do I register in California (PIN-by-mail)?": "how-do-i-register-in-california-pin-by-mail",
    "How do I track nexus thresholds in real time across all my sales channels?": "how-do-i-track-nexus-thresholds-in-real-time",
    "How do I use the MTC multi-state VDA program?": "how-do-i-use-the-mtc-multi-state-vda-program",
    "How do I validate an exemption certificate?": "how-do-i-validate-an-exemption-certificate",
    "How do US sales tax obligations change when I expand internationally?": "how-do-us-sales-tax-obligations-change-when-i-expand-internationally",
    "How does Shopify handle sales tax?": "how-does-shopify-handle-sales-tax",
    "How does a CSP's audit liability shield work in SST states?": "how-does-a-csps-audit-liability-shield-work-in-sst-states",
    "How far back do I owe sales tax if I haven't been collecting?": "how-far-back-do-i-owe-sales-tax",
    "How is the nexus threshold calculated, calendar year or trailing 12 months?": "how-is-the-nexus-threshold-calculated-calendar-year-or-trailing-12-months",
    "How long can a state audit go back?": "how-long-can-a-state-audit-go-back",
    "How long does it take to get a sales tax permit in each state?": "how-long-does-it-take-to-get-a-sales-tax-permit",
    "I haven't been collecting sales tax — what do I do now?": "i-havent-been-collecting-sales-tax-what-do-i-do-now",
    "I haven't been collecting sales tax, what do I do now?": "i-havent-been-collecting-sales-tax-what-do-i-do-now",
    "I haven't been collecting, what do I do now?": "i-havent-been-collecting-sales-tax-what-do-i-do-now",
    "Is there a grace period between crossing a threshold and registering?": "is-there-a-grace-period-between-crossing-threshold-and-registering",
    "Is there a grace period between crossing a threshold and when I must register?": "is-there-a-grace-period-between-crossing-threshold-and-registering",
    "Is there a grace period between crossing and when I must register?": "is-there-a-grace-period-between-crossing-threshold-and-registering",
    "Registered mid-month: when does my sales tax obligation start?": "registered-mid-month-when-does-sales-tax-obligation-start",
    "Should I hire a CPA or tax attorney for a sales tax audit?": "should-i-hire-a-cpa-or-tax-attorney-for-a-sales-tax-audit",
    "What are the penalties for not collecting sales tax?": "what-are-the-penalties-for-not-collecting-sales-tax",
    "What does sales tax compliance actually cost?": "what-does-sales-tax-compliance-actually-cost",
    "What does the back-filing process actually look like?": "what-does-the-back-filing-process-look-like",
    "What does the back-filing process look like?": "what-does-the-back-filing-process-look-like",
    "What happens if I was supposed to register earlier and didn't?": "what-happens-if-i-was-supposed-to-register-earlier-and-didnt",
    "What if I sell through multiple channels?": "what-if-i-sell-through-multiple-channels",
    "What is Shopify Tax and how does it differ from basic settings?": "what-is-shopify-tax-and-how-does-it-differ-from-basic-settings",
    "What is Shopify Tax, and how does it differ from basic tax settings?": "what-is-shopify-tax-and-how-does-it-differ-from-basic-settings",
    "What is a Certified Service Provider?": "what-is-a-certified-service-provider",
    "What is a direct pay permit?": "what-is-a-direct-pay-permit",
    "What is a marketplace facilitator law and does it apply to me?": "what-is-a-marketplace-facilitator-law",
    "What is a marketplace facilitator law?": "what-is-a-marketplace-facilitator-law",
    "What is a prepayment requirement in sales tax?": "what-is-a-prepayment-requirement-in-sales-tax",
    "What is a sales tax rate and what does it include?": "what-is-a-sales-tax-rate-and-what-does-it-include",
    "What is an exemption certificate?": "what-is-an-exemption-certificate",
    "What is an international seller's US sales tax obligation?": "what-is-an-international-sellers-us-sales-tax-obligation",
    "What is economic nexus and how does it differ from physical nexus?": "what-is-economic-nexus",
    "What is economic nexus and how does it work?": "what-is-economic-nexus",
    "What is economic nexus?": "what-is-economic-nexus",
    "What is sales tax and how does it work for online stores?": "what-is-sales-tax-and-how-does-it-work-for-online-stores",
    "What is the Avalara separation process, what exact steps are involved?": "what-is-the-avalara-separation-process",
    "What is the Avalara separation process?": "what-is-the-avalara-separation-process",
    "What is the SST Exemption Certificate?": "what-is-the-sst-exemption-certificate",
    "What is the Wayfair ruling in more detail?": "what-is-the-wayfair-ruling",
    "What records does a state auditor request?": "what-records-does-a-state-auditor-request",
    "What should I do if I receive a sales tax notice?": "what-should-i-do-if-i-receive-a-sales-tax-notice",
    "What triggers a sales tax audit?": "what-triggers-a-sales-tax-audit",
    "When does economic nexus begin: the day I cross or the next period?": "when-does-economic-nexus-begin",
    "When does economic nexus begin: the day I cross the threshold or the next period?": "when-does-economic-nexus-begin",
    "When does sales tax liability accrue, at order, fulfillment, or payment?": "when-does-sales-tax-liability-accrue-order-fulfillment-or-payment",
    "When does sales tax liability accrue, order placement, fulfillment, or payment?": "when-does-sales-tax-liability-accrue-order-fulfillment-or-payment",
    "Which marketplaces are covered by facilitator laws in all states?": "which-marketplaces-are-covered-by-facilitator-laws-in-all-states",
    "Which states tax SaaS and which don't?": "which-states-tax-saas-and-which-dont",
    "Who is responsible for collecting sales tax?": "who-is-responsible-for-collecting-sales-tax",
    "Why does Colorado charge a credit card fee on sales tax payments?": "why-does-colorado-charge-a-credit-card-fee-on-sales-tax-payments",
    "Why does SST require monthly filing?": "why-does-sst-require-monthly-filing",
    "Why doesn't marketplace facilitation completely eliminate my compliance obligations?": "why-doesnt-marketplace-facilitation-eliminate-compliance-obligations",
    "Why doesn't marketplace facilitation eliminate my compliance obligations?": "why-doesnt-marketplace-facilitation-eliminate-compliance-obligations",
    "Why won't Avalara and TaxJar tell me about SST benefits?": "why-wont-avalara-taxjar-tell-me-about-sst-benefits",
    "Will there be a compliance gap when switching providers mid-year?": "will-there-be-a-compliance-gap-switching-providers",
    "Will there be a compliance gap when switching providers?": "will-there-be-a-compliance-gap-switching-providers",
    "Will there be a compliance gap when switching sales tax providers?": "will-there-be-a-compliance-gap-switching-providers",
    "Can I just start collecting going forward without addressing the past?": "can-i-just-start-collecting-sales-tax-going-forward",
    "Can I just start collecting sales tax going forward without addressing the past?": "can-i-just-start-collecting-sales-tax-going-forward",
    "Can I just start collecting sales tax going forward?": "can-i-just-start-collecting-sales-tax-going-forward",
    "Can I pass sales tax costs on to customers?": "can-i-pass-sales-tax-costs-on-to-customers",
    "Can I choose my own filing frequency?": "can-i-choose-my-own-filing-frequency",
    "Are food items taxable?": "are-food-items-taxable",
    "Are services taxable?": "are-services-taxable",
    "Is streaming content taxable?": "is-streaming-content-taxable",
    "Do I need exemption certificates from nonprofits and universities?": "do-i-need-exemption-certificates-from-nonprofits-and-universities",
    "Do I need a separate permit for every state?": "do-i-need-a-separate-permit-for-every-state",
    "Do marketplace sales count toward my nexus threshold?": "do-marketplace-sales-count-toward-my-nexus-threshold",
    "Do trade shows trigger sales tax nexus?": "do-trade-shows-trigger-sales-tax-nexus",
    "Does Amazon FBA inventory create nexus in states where it's stored?": "does-amazon-fba-inventory-create-nexus",
    "Does Amazon cover all states, or are there gaps?": "does-amazon-cover-all-states-or-are-there-gaps",
    "Does drop shipping create physical nexus for the retailer?": "does-drop-shipping-create-physical-nexus",
    "Does drop shipping create physical nexus?": "does-drop-shipping-create-physical-nexus",
    "Does having a sales rep or affiliate create nexus?": "does-having-a-sales-rep-or-affiliate-create-nexus",
    "Does having a sales rep or affiliate in another state create nexus?": "does-having-a-sales-rep-or-affiliate-create-nexus",
    "Does selling on Etsy mean I don't have to worry about sales tax?": "does-selling-on-etsy-mean-i-dont-have-to-worry-about-sales-tax",
    "Does selling wholesale exempt me from collecting sales tax?": "does-selling-wholesale-exempt-me-from-collecting-sales-tax",
    "How are bundled products taxed?": "how-are-bundled-products-taxed",
    "How are subscription boxes taxed?": "how-are-subscription-boxes-taxed",
    "How do I aggregate nexus thresholds across Amazon, Shopify, Etsy, and Walmart?": "how-do-i-aggregate-nexus-thresholds-across-channels",
    "Do I need to file a zero return if I have nexus but no sales in a given month?": "do-i-need-to-file-a-zero-return-if-i-have-no-sales",
}

total_replaced = 0
still_unmatched = set()

mdx_files = glob.glob(f"{CONTENT_DIR}/**/*.mdx", recursive=True)
pattern = re.compile(r'\[([^\]]+)\]\(#\)')

for filepath in sorted(mdx_files):
    with open(filepath, "r") as f:
        content = f.read()

    if "(#)" not in content:
        continue

    def replace_link(m):
        global total_replaced
        link_text = m.group(1)
        if link_text in MANUAL_MAP:
            total_replaced += 1
            return f"[{link_text}](/{MANUAL_MAP[link_text]})"
        still_unmatched.add(link_text)
        return m.group(0)

    new_content = pattern.sub(replace_link, content)

    if new_content != content:
        with open(filepath, "w") as f:
            f.write(new_content)

print(f"Replaced: {total_replaced} additional links")
print(f"Remaining (#) links: {len(still_unmatched)}")
if still_unmatched:
    print("\nStill unresolved:")
    for t in sorted(still_unmatched):
        print(f"  - {t}")
