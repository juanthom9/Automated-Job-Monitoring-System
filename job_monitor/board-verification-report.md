# Job board verification report

A live connector proves that an endpoint works. `confirmed` additionally means the
official careers path exposed the same supported ATS. Other live boards require
manual ownership verification before they should be considered fully confirmed.

## Summary

| Status | Count |
|---|---:|
| confirmed | 38 |
| connector_failed | 1 |
| disabled | 4 |
| empty_unconfirmed | 1 |
| live_unconfirmed | 101 |

## Companies

| Company | Configured | Discovered | Jobs | Status | Evidence / detail |
|---|---|---|---:|---|---|
| 1Password | ashby | ashby | 62 | confirmed | https://jobs.ashbyhq.com/1password |
| Accenture | workday | workday | 40 | confirmed | https://accenture.wd103.myworkdayjobs.com/AccentureCareers/userHome |
| Activision | workday | workday | 2 | confirmed | https://xboxgaming.wd1.myworkdayjobs.com/CentralTech/ |
| Anthropic | greenhouse | greenhouse | 587 | confirmed | https://job-boards.greenhouse.io/anthropic/jobs/4980436008 |
| Arctic Wolf | workday | workday | 115 | confirmed | https://arcticwolf.wd1.myworkdayjobs.com/External |
| Autodesk | workday | workday | 40 | confirmed | https://autodesk.wd1.myworkdayjobs.com/Ext |
| BlackBerry | workday | workday | 31 | confirmed | https://bb.wd3.myworkdayjobs.com/BlackBerry/jobs |
| Blizzard Entertainment | workday | workday | 36 | confirmed | https://xboxgaming.wd1.myworkdayjobs.com/Blizzard_External_Careers/job/Irvine---Blizzard---Blizzard-Way/Manager--Finance---Blizzard---Irvine--CA_R026703/apply |
| Cadence Design Systems | workday | workday | 40 | confirmed | https://cadence.wd1.myworkdayjobs.com/External_Careers |
| CD PROJEKT | smartrecruiters | smartrecruiters | 44 | confirmed | https://jobs.smartrecruiters.com/CDPROJEKTRED/743999834254914-spontaneous-application |
| CIBC | workday | workday | 40 | confirmed | https://cibc.wd3.myworkdayjobs.com/search?q=banking+centre&jobFamilyGroup=4bbe6c74e8a7011d49ad22a881011310&jobFamilyGroup=4bbe6c74e8a70132da752ca881011910&Country=a30a87ed25634629aa6c3958aa2b91ea |
| Clearco | ashby | ashby | 3 | confirmed | https://jobs.ashbyhq.com/clearco/embed |
| Cohere | ashby | ashby | 144 | confirmed | https://jobs.ashbyhq.com/cohere |
| EQ Bank | lever | lever | 67 | confirmed | https://jobs.lever.co/eqbank |
| Figma | greenhouse | greenhouse | 158 | confirmed | https://boards.greenhouse.io/figma/jobs/5813967004?gh_jid=5813967004 |
| GeoComply | lever | lever | 7 | confirmed | https://jobs.lever.co/geocomply-2/1011f998-83cb-475a-9026-879bbe2e4220 |
| Intel | workday | workday | 76 | confirmed | https://intel.wd1.myworkdayjobs.com/External/page/6042070b79e01001f04fa9b468070000 |
| Juniper Networks | workday | workday | 40 | confirmed | https://hpe.wd5.myworkdayjobs.com/Jobsathpe/job/Bengaluru-Karntaka-India/Senior-Software-Engineer---Networking_1198267-1/apply |
| King | workday | workday | 15 | confirmed | https://xboxgaming.wd1.myworkdayjobs.com/King_External_Careers/job/Stockholm---King---Malmskillnadsgatan/Senior-Manager--Product-Marketing---New-Games--Stockholm--On-site-_R027868/apply |
| Linear | ashby | ashby | 29 | confirmed | https://jobs.ashbyhq.com/Linear/c21af93e-210f-4969-8eaa-90fb16a5b720\ |
| Mastercard | workday | workday | 40 | confirmed | https://mastercard.wd1.myworkdayjobs.com/CorporateCareers |
| Mercury | greenhouse | greenhouse | 59 | confirmed | https://job-boards.greenhouse.io/mercury/jobs/6122010004 |
| New Relic | greenhouse | greenhouse | 52 | confirmed | https://job-boards.greenhouse.io/newrelic/jobs/5142016008 |
| Notion | ashby | ashby | 130 | confirmed | https://jobs.ashbyhq.com/notion/05e14247-17c4-4e98-9a13-53828a4e2f13 |
| NVIDIA | workday | workday | 40 | confirmed | https://nvidia.wd5.myworkdayjobs.com/NVIDIAExternalCareerSite |
| Ramp | ashby | ashby | 141 | confirmed | https://jobs.ashbyhq.com/ramp/34413f8d-26bf-4bbc-8ade-eb309a0e2245\ |
| Red Hat | workday | workday | 40 | confirmed | https://redhat.wd5.myworkdayjobs.com/Jobs/assets/logo |
| Snowflake | ashby | ashby | 370 | confirmed | https://jobs.ashbyhq.com/snowflake/0636f234-a5d9-4c8f-8516-f2eddf3b8d4c |
| Sony Interactive Entertainment (PlayStation) | greenhouse | greenhouse | 2 | confirmed | https://job-boards.greenhouse.io/siei/jobs/6138372004 |
| Supabase | ashby | ashby | 60 | confirmed | https://jobs.ashbyhq.com/supabase/23c9ce7e-6b7b-4316-8f00-8f318e902441 |
| TD Bank | workday | workday | 114 | confirmed | https://td.wd3.myworkdayjobs.com/en-US/TD_Bank_Careers |
| Unity | workday | workday | 123 | confirmed | https://unitytech.wd1.myworkdayjobs.com/Unity/job/Bengaluru-India/Accountant_JOBREQ-2615595\ |
| Vercel | greenhouse | greenhouse | 89 | confirmed | https://job-boards.greenhouse.io/vercel/jobs/6136160004\ |
| Visa | workday | workday | 40 | confirmed | https://visa.wd5.myworkdayjobs.com/Visa |
| Wattpad | lever | lever | 6 | confirmed | https://jobs.lever.co/wattpad |
| Wealthsimple | ashby | ashby | 49 | confirmed | https://jobs.ashbyhq.com/wealthsimple |
| Workday | workday | workday | 40 | confirmed | https://workday.wd5.myworkdayjobs.com/Workday |
| Zillow | workday | workday | 40 | confirmed | https://zillow.wd5.myworkdayjobs.com/Zillow_Group_External |
| Microsoft | microsoft |  |  | connector_failed | HTTPStatusError: Client error '429 Too Many Requests' for url 'https://apply.careers.microsoft.com/api/pcsx/search?domain=microsoft.com&query=intern&location=&start=0&sort_by=relevance' For more information check: https://developer.mozilla.org/en-US/docs/Web/HTTP/Status/429 |
| LinkedIn | unsupported |  |  | disabled | Company is intentionally disabled or unresolved |
| Meta | unsupported |  |  | disabled | Company is intentionally disabled or unresolved |
| Tesla | unsupported |  |  | disabled | Company is intentionally disabled or unresolved |
| Uber | unsupported |  |  | disabled | Company is intentionally disabled or unresolved |
| HashiCorp | ibm |  | 0 | empty_unconfirmed | No supported ATS link was exposed by the careers page |
| Ada | greenhouse |  | 9 | live_unconfirmed | No supported ATS link was exposed by the careers page |
| Adobe | workday |  | 6 | live_unconfirmed | No supported ATS link was exposed by the careers page |
| Affirm | greenhouse |  | 199 | live_unconfirmed | No supported ATS link was exposed by the careers page |
| Airbnb | greenhouse |  | 172 | live_unconfirmed | No supported ATS link was exposed by the careers page |
| Amazon | amazon |  | 206 | live_unconfirmed | No supported ATS link was exposed by the careers page |
| AMD | phenom |  | 89 | live_unconfirmed | No supported ATS link was exposed by the careers page |
| Anduril | greenhouse |  | 2207 | live_unconfirmed | No supported ATS link was exposed by the careers page |
| Apple | apple |  | 64 | live_unconfirmed | No supported ATS link was exposed by the careers page |
| Arm | talentbrew |  | 46 | live_unconfirmed | No supported ATS link was exposed by the careers page |
| Atlassian | jibe |  | 224 | live_unconfirmed | No supported ATS link was exposed by the careers page |
| Behaviour Interactive | lever |  | 38 | live_unconfirmed | No supported ATS link was exposed by the careers page |
| Bell | phenom_widget |  | 50 | live_unconfirmed | No supported ATS link was exposed by the careers page |
| Block | greenhouse |  | 203 | live_unconfirmed | No supported ATS link was exposed by the careers page |
| BMO | workday |  | 72 | live_unconfirmed | No supported ATS link was exposed by the careers page |
| Box | greenhouse |  | 146 | live_unconfirmed | No supported ATS link was exposed by the careers page |
| Brex | greenhouse |  | 282 | live_unconfirmed | No supported ATS link was exposed by the careers page |
| Bungie | greenhouse |  | 3 | live_unconfirmed | No supported ATS link was exposed by the careers page |
| Canva | smartrecruiters |  | 267 | live_unconfirmed | No supported ATS link was exposed by the careers page |
| CGI | jobsyn |  | 20 | live_unconfirmed | No supported ATS link was exposed by the careers page |
| Clio | workday |  | 128 | live_unconfirmed | No supported ATS link was exposed by the careers page |
| Cloudflare | greenhouse |  | 331 | live_unconfirmed | No supported ATS link was exposed by the careers page |
| Coinbase | greenhouse |  | 192 | live_unconfirmed | No supported ATS link was exposed by the careers page |
| Confluent | confluent |  | 22 | live_unconfirmed | No supported ATS link was exposed by the careers page |
| Cruise | workday |  | 57 | live_unconfirmed | No supported ATS link was exposed by the careers page |
| Databricks | greenhouse |  | 872 | live_unconfirmed | No supported ATS link was exposed by the careers page |
| Deloitte | deloitte |  | 450 | live_unconfirmed | No supported ATS link was exposed by the careers page |
| Descartes Systems Group | successfactors |  | 32 | live_unconfirmed | No supported ATS link was exposed by the careers page |
| Discord | greenhouse |  | 48 | live_unconfirmed | No supported ATS link was exposed by the careers page |
| ecobee | workday |  | 18 | live_unconfirmed | No supported ATS link was exposed by the careers page |
| Elastic | greenhouse |  | 358 | live_unconfirmed | No supported ATS link was exposed by the careers page |
| Electronic Arts | avature |  | 323 | live_unconfirmed | No supported ATS link was exposed by the careers page |
| Epic Games | greenhouse |  | 158 | live_unconfirmed | No supported ATS link was exposed by the careers page |
| Ericsson | eightfold |  | 52 | live_unconfirmed | No supported ATS link was exposed by the careers page |
| Expedia Group | workday |  | 134 | live_unconfirmed | No supported ATS link was exposed by the careers page |
| EY | yello |  | 70 | live_unconfirmed | No supported ATS link was exposed by the careers page |
| Faire | greenhouse |  | 60 | live_unconfirmed | No supported ATS link was exposed by the careers page |
| Garmin | jibe |  | 365 | live_unconfirmed | No supported ATS link was exposed by the careers page |
| GitHub | jibe |  | 85 | live_unconfirmed | No supported ATS link was exposed by the careers page |
| GitLab | greenhouse |  | 228 | live_unconfirmed | No supported ATS link was exposed by the careers page |
| Glean | greenhouse |  | 114 | live_unconfirmed | No supported ATS link was exposed by the careers page |
| Google | google |  | 44 | live_unconfirmed | No supported ATS link was exposed by the careers page |
| Hex | ashby |  | 31 | live_unconfirmed | No supported ATS link was exposed by the careers page |
| Hootsuite | greenhouse |  | 24 | live_unconfirmed | No supported ATS link was exposed by the careers page |
| IBM | ibm |  | 274 | live_unconfirmed | No supported ATS link was exposed by the careers page |
| Insomniac Games | greenhouse |  | 6 | live_unconfirmed | No supported ATS link was exposed by the careers page |
| Intuit | intuit |  | 23 | live_unconfirmed | No supported ATS link was exposed by the careers page |
| Kinaxis | jibe |  | 100 | live_unconfirmed | No supported ATS link was exposed by the careers page |
| KPMG | kpmg |  | 518 | live_unconfirmed | No supported ATS link was exposed by the careers page |
| Loblaw Digital | paradox |  | 21 | live_unconfirmed | No supported ATS link was exposed by the careers page |
| Lucid Motors | greenhouse |  | 323 | live_unconfirmed | No supported ATS link was exposed by the careers page |
| Lyft | greenhouse |  | 167 | live_unconfirmed | No supported ATS link was exposed by the careers page |
| MathWorks | mathworks |  | 2 | live_unconfirmed | No supported ATS link was exposed by the careers page |
| MongoDB | greenhouse |  | 406 | live_unconfirmed | No supported ATS link was exposed by the careers page |
| National Bank of Canada | avature |  | 79 | live_unconfirmed | No supported ATS link was exposed by the careers page |
| NetApp | talentbrew |  | 21 | live_unconfirmed | No supported ATS link was exposed by the careers page |
| Netflix | netflix |  | 4 | live_unconfirmed | No supported ATS link was exposed by the careers page |
| Nintendo | greenhouse |  | 52 | live_unconfirmed | No supported ATS link was exposed by the careers page |
| Nokia | oracle_hcm |  | 222 | live_unconfirmed | No supported ATS link was exposed by the careers page |
| Okta | greenhouse |  | 310 | live_unconfirmed | No supported ATS link was exposed by the careers page |
| OpenAI | ashby |  | 781 | live_unconfirmed | No supported ATS link was exposed by the careers page |
| OpenText | phenom_widget |  | 342 | live_unconfirmed | No supported ATS link was exposed by the careers page |
| Oracle | oracle_hcm |  | 1967 | live_unconfirmed | No supported ATS link was exposed by the careers page |
| Palantir Technologies | lever |  | 310 | live_unconfirmed | No supported ATS link was exposed by the careers page |
| PayPal | workday |  | 40 | live_unconfirmed | No supported ATS link was exposed by the careers page |
| Perplexity | ashby |  | 112 | live_unconfirmed | No supported ATS link was exposed by the careers page |
| Pinterest | greenhouse |  | 187 | live_unconfirmed | No supported ATS link was exposed by the careers page |
| Plaid | plaid |  | 103 | live_unconfirmed | No supported ATS link was exposed by the careers page |
| PointClickCare | lever |  | 80 | live_unconfirmed | No supported ATS link was exposed by the careers page |
| Pure Storage | greenhouse |  | 321 | live_unconfirmed | No supported ATS link was exposed by the careers page |
| PwC | workday |  | 202 | live_unconfirmed | No supported ATS link was exposed by the careers page |
| Qualcomm | eightfold |  | 54 | live_unconfirmed | No supported ATS link was exposed by the careers page |
| RBC | workday |  | 40 | live_unconfirmed | No supported ATS link was exposed by the careers page |
| Redfin | phenom_widget |  | 263 | live_unconfirmed | No supported ATS link was exposed by the careers page |
| Replicate | greenhouse |  | 2 | live_unconfirmed | No supported ATS link was exposed by the careers page |
| Riot Games | greenhouse |  | 106 | live_unconfirmed | No supported ATS link was exposed by the careers page |
| Rivian | jibe |  | 732 | live_unconfirmed | No supported ATS link was exposed by the careers page |
| Robinhood | greenhouse |  | 127 | live_unconfirmed | No supported ATS link was exposed by the careers page |
| Roblox | greenhouse |  | 231 | live_unconfirmed | No supported ATS link was exposed by the careers page |
| Rockstar Games | greenhouse |  | 64 | live_unconfirmed | No supported ATS link was exposed by the careers page |
| Rogers Communications | successfactors |  | 87 | live_unconfirmed | No supported ATS link was exposed by the careers page |
| Salesforce | workday |  | 34 | live_unconfirmed | No supported ATS link was exposed by the careers page |
| SAP | successfactors |  | 146 | live_unconfirmed | No supported ATS link was exposed by the careers page |
| Scotiabank | successfactors |  | 955 | live_unconfirmed | No supported ATS link was exposed by the careers page |
| ServiceNow | smartrecruiters |  | 603 | live_unconfirmed | No supported ATS link was exposed by the careers page |
| Shopify | shopify |  | 110 | live_unconfirmed | No supported ATS link was exposed by the careers page |
| SpaceX | greenhouse |  | 2340 | live_unconfirmed | No supported ATS link was exposed by the careers page |
| Splunk | phenom_widget |  | 1 | live_unconfirmed | No supported ATS link was exposed by the careers page |
| Stripe | greenhouse |  | 617 | live_unconfirmed | No supported ATS link was exposed by the careers page |
| Synopsys | talentbrew |  | 13 | live_unconfirmed | No supported ATS link was exposed by the careers page |
| Take-Two Interactive | greenhouse |  | 38 | live_unconfirmed | No supported ATS link was exposed by the careers page |
| ThinkOn | adp_workforce_now |  | 7 | live_unconfirmed | No supported ATS link was exposed by the careers page |
| Twilio | greenhouse |  | 149 | live_unconfirmed | No supported ATS link was exposed by the careers page |
| Ubisoft | smartrecruiters |  | 274 | live_unconfirmed | No supported ATS link was exposed by the careers page |
| Valve | valve |  | 26 | live_unconfirmed | No supported ATS link was exposed by the careers page |
| Visier | greenhouse |  | 11 | live_unconfirmed | No supported ATS link was exposed by the careers page |
| Waymo | greenhouse |  | 343 | live_unconfirmed | No supported ATS link was exposed by the careers page |
| xAI | greenhouse |  | 256 | live_unconfirmed | No supported ATS link was exposed by the careers page |
| Yelp | phenom_widget |  | 53 | live_unconfirmed | No supported ATS link was exposed by the careers page |
| Zoox | lever |  | 240 | live_unconfirmed | No supported ATS link was exposed by the careers page |
| Cisco | phenom_widget |  | 18 | live_unconfirmed | No supported ATS link was exposed by the careers page |
| TELUS | successfactors |  | 24 | live_unconfirmed | No supported ATS link was exposed by the careers page |
