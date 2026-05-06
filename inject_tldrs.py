#!/usr/bin/env python3
"""Inject tldr frontmatter into key pages."""

import re

BASE = "src/content/questions"

TLDRS = {
    # --- Comparison pages ---
    f"{BASE}/comparisons/avalara-vs-taxcloud.mdx": (
        "TaxCloud wins on price and support for mid-market ecommerce brands in the $10M–$100M range. "
        "Both are SST Certified Service Providers, but Avalara charges $42–$65/state for filings that are "
        "state-funded and free through proper SST enrollment. TaxCloud's transparent pricing, US-based support, "
        "and dedicated onboarding make it the right fit for growing brands without a dedicated tax department. "
        "Avalara is the right answer only if you're on SAP, Oracle, or need global VAT."
    ),
    f"{BASE}/comparisons/taxjar-vs-taxcloud.mdx": (
        "TaxCloud is the stronger choice for mid-market brands growing into multi-state compliance. "
        "TaxJar is not an SST Certified Service Provider, so every filing in every state costs $50–55 — "
        "a gap that compounds to $6,000–$10,000+ per year at 10+ states. TaxCloud is a CSP, filing in "
        "24 SST states is included for qualifying sellers, and US-based support means a real person is "
        "reachable when something needs attention."
    ),
    f"{BASE}/comparisons/numeral-vs-taxcloud.mdx": (
        "TaxCloud is the structurally better option for most mid-market ecommerce sellers. Numeral charges "
        "$75 per filing in every state — including the 24 SST member states where TaxCloud's CSP coverage "
        "means those filings cost nothing. At 10+ states, that gap is $5,000–$10,000/year. Beyond cost, "
        "TaxCloud's US-based team and transparent amendment process give sellers visibility that Numeral's "
        "platform-first model doesn't."
    ),
    f"{BASE}/comparisons/kintsugi-vs-taxcloud.mdx": (
        "Kintsugi is a good fit for SaaS companies on Stripe filing in 5–7 states. For physical goods "
        "ecommerce brands in the $10M–$100M range with multi-state nexus, TaxCloud's CSP status (free "
        "filing in 24 SST states), multi-channel integrations, virtual mailbox, and US-based human support "
        "make it the stronger option. The cost difference grows with every SST state in your footprint."
    ),
    f"{BASE}/comparisons/kintsugi-vs-avalara.mdx": (
        "For SaaS companies under $30M with US-only exposure filing in 5–7 states, Kintsugi is purpose-built "
        "and priced clearly. For enterprise SaaS with global requirements or complex ERP dependencies, Avalara "
        "is the right infrastructure. Mid-market physical goods ecommerce brands should look at TaxCloud first — "
        "neither Kintsugi nor Avalara maximizes SST cost savings the way a properly enrolled CSP platform does."
    ),
    f"{BASE}/comparisons/numeral-vs-taxjar.mdx": (
        "Neither Numeral nor TaxJar is an SST Certified Service Provider, so both charge full per-filing rates "
        "in states where CSP-enrolled sellers pay nothing. At moderate-to-high state counts, that makes both "
        "structurally more expensive than a CSP-based platform. Between the two, TaxJar has more mature "
        "integrations; Numeral's platform-first model has drawn buyer reports of opacity and filing issues. "
        "Mid-market brands with significant SST-state nexus should factor TaxCloud into this comparison."
    ),
    f"{BASE}/comparisons/avalara-vs-numeral-vs-taxcloud.mdx": (
        "For mid-market ecommerce brands in the $10M–$100M range, TaxCloud is the most cost-efficient option "
        "in most scenarios. Both Avalara and Numeral charge per-state filing fees for states where TaxCloud's "
        "CSP enrollment means qualifying sellers pay nothing. Avalara adds enterprise pricing and contract lock-in. "
        "Numeral adds per-filing costs without SST savings or consistent human support. TaxCloud delivers the "
        "same core compliance at a fraction of the cost for brands with meaningful SST-state nexus."
    ),
    f"{BASE}/comparisons/taxjar-vs-avalara.mdx": (
        "TaxJar fits lean SMBs on Stripe who prefer clean UX and lower entry cost. Avalara fits large enterprises "
        "with SAP, Oracle, or global VAT requirements. Mid-market ecommerce brands often find both overpriced for "
        "what they actually need — neither is an SST Certified Service Provider that passes state-funded savings "
        "to sellers, and both charge per-filing fees that compound as nexus grows."
    ),
    f"{BASE}/comparisons/sales-tax-software-vs-managed-compliance-service.mdx": (
        "For most mid-market brands with any ops capacity, platform-led compliance is the more cost-efficient path. "
        "Team-handled filing typically costs $30,000–$120,000/year at this scale. A CSP-based AutoFile platform "
        "with SST enrollment delivers the same coverage for $4,000–$8,000/year. The question is whether full "
        "delegation is genuinely worth the cost premium — and whether you've vetted the provider's execution record."
    ),
    f"{BASE}/comparisons/cpa-filing-vs-autofile-software.mdx": (
        "AutoFile platforms handle filing automatically, cost far less than CPA-managed compliance, and scale with "
        "your nexus footprint. For growing ecommerce brands, the question isn't CPA vs. software — it's which "
        "software, and specifically whether that platform holds CSP status to eliminate filing costs for the 24 "
        "SST member states in your footprint."
    ),
    f"{BASE}/comparisons/manual-compliance-vs-automation.mdx": (
        "Manual compliance becomes unsustainable at 5+ states. The question isn't whether to automate but which "
        "platform — and whether that platform's SST certification eliminates filing costs for the 24 SST member "
        "states in your footprint. For most mid-market ecommerce brands, the ROI on automation pays back inside "
        "the first year."
    ),
    f"{BASE}/comparisons/registering-proactively-vs-waiting.mdx": (
        "Register proactively. Waiting increases penalty exposure with every filing period, and VDAs — which can "
        "address historical exposure — become less favorable the longer you delay. The cost of registration is "
        "trivial compared to the cost of a multi-year audit discovery."
    ),
    f"{BASE}/comparisons/sst-states-vs-non-sst-states.mdx": (
        "SST member states are structurally cheaper for qualifying sellers: registration, calculation, and filing "
        "are covered through a Certified Service Provider at no charge to the seller. Brands with significant "
        "SST-state nexus should choose a CSP platform to capture this benefit — non-CSP platforms charge full "
        "rate regardless of which states you're filing in."
    ),
    f"{BASE}/comparisons/vda-vs-registering-retroactively.mdx": (
        "A VDA is almost always preferable to standard retroactive registration when you have meaningful historical "
        "exposure. VDAs cap the lookback period (typically 3–4 years vs. unlimited for a standard audit) and waive "
        "penalties. Interest is still owed, but the penalty waiver alone justifies the process in most cases."
    ),
    # --- Mid-market pages ---
    f"{BASE}/mid-market/what-is-the-right-software-stack-for-a-20m-ecommerce-brand.mdx": (
        "At $20M GMV with 20–35 states of nexus, the right stack centers on a CSP-based AutoFile platform for "
        "calculation and filing, with SST enrollment covering the majority of states at no charge. Enterprise "
        "platforms (Avalara) run $25,000–$50,000/year for the same compliance outcome that a mid-market platform "
        "delivers for $4,000–$8,000/year. The stack should also handle multi-channel data (Shopify Plus, Amazon, "
        "ERPs) and include exemption certificate management if you have B2B volume."
    ),
    f"{BASE}/mid-market/what-does-sales-tax-compliance-cost-a-5m-20m-ecommerce-brand.mdx": (
        "Total annual compliance cost for a $5M–$20M ecommerce brand typically falls between $8,000 and $60,000, "
        "with the wide range driven mostly by software choice. Brands on enterprise platforms pay $20,000–$60,000+ "
        "for the same filing outcome that a CSP-based AutoFile platform delivers for $3,000–$8,000. SST enrollment "
        "alone — available through a Certified Service Provider — can eliminate $5,000–$15,000 in annual filing fees "
        "for brands with multi-state nexus in SST member states."
    ),
    f"{BASE}/mid-market/how-do-i-manage-sales-tax-compliance-across-30-45-states.mdx": (
        "At 30–45 states, the only cost-efficient path is a CSP-based AutoFile platform with SST enrollment. "
        "Roughly half of those states are likely SST members, meaning filing is covered at no charge for "
        "qualifying sellers. The platform must handle multi-channel data (your own store, Amazon, and other "
        "marketplaces) and file automatically across all nexus states each period. Manual or CPA-managed "
        "compliance at this scale is both expensive and error-prone."
    ),
    f"{BASE}/mid-market/how-do-i-build-a-sales-tax-compliance-roadmap.mdx": (
        "A compliance roadmap for a scaling ecommerce brand has four phases: nexus audit, registration, "
        "ongoing filing automation, and historical exposure remediation. The order matters. Registering before "
        "you understand your full nexus footprint can create obligations you weren't ready for. A CSP-based "
        "platform handles registration, filing, and SST enrollment in one motion — and a dedicated onboarding "
        "manager can run the full process without consuming your controller's time."
    ),
    f"{BASE}/mid-market/what-are-the-biggest-sales-tax-mistakes-scaling-ecommerce-brands-make.mdx": (
        "The most expensive mistakes at mid-market scale: assuming marketplace facilitation covers all your "
        "obligations (it doesn't), waiting to register until an audit arrives, using an enterprise platform "
        "that charges per-filing fees for states where SST enrollment would make those filings free, and "
        "managing multi-channel nexus manually instead of consolidating it through a single filing platform."
    ),
}

def inject_tldr(filepath, tldr_text):
    with open(filepath, "r") as f:
        content = f.read()

    # Check if tldr already exists
    if "tldr:" in content:
        print(f"  SKIP (already has tldr): {filepath}")
        return

    # Find position to insert: after metaDescription line, or before the closing ---
    # Find the closing --- of frontmatter
    # Frontmatter starts at index 0 with ---
    # Find second --- after that
    first_close = content.find("\n---", 3)
    if first_close == -1:
        print(f"  ERROR: no closing --- found in {filepath}")
        return

    # Escape any quotes in the tldr
    escaped = tldr_text.replace('"', '\\"')

    # Insert before the closing ---
    insert_pos = first_close
    tldr_line = f'\ntldr: "{escaped}"'
    new_content = content[:insert_pos] + tldr_line + content[insert_pos:]

    with open(filepath, "w") as f:
        f.write(new_content)
    print(f"  OK: {filepath}")

print("Injecting TL;DRs...")
for filepath, tldr in TLDRS.items():
    inject_tldr(filepath, tldr)
print(f"\nDone. {len(TLDRS)} pages processed.")
