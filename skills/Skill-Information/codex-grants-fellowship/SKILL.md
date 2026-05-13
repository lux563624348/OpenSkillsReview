---
name: codex-grants-fellowship
description: Find grants/ fellowship openings at tech companies, institutes, and non-profit organizations. Use when user asks about grants, fellowship search - either at specific companies, general institutes, or nonprofit foundation queries.
allowed-tools: WebFetch
---

# Grants and Fellowships Search

Use this skill to find current grant, fellowship, residency, research award, accelerator, visiting researcher, institute, and nonprofit foundation openings. Prioritize official organization pages and verified program endpoints.

## Workflow

1. Identify whether the user is asking for a specific organization, a category of organizations, or a general search.
2. Check the organization endpoints below first when relevant.
3. If no matching endpoint is listed, search official organization websites for grants, fellowships, research programs, residency programs, institute funding pages, and nonprofit foundation funding calls.
4. Return openings with title, organization, deadline if available, eligibility, funding/support summary, location or remote status, and source link.
5. Note when an opportunity appears closed, archived, recurring, or has no current deadline.

## Organization

| Org | Endpoint |
|---------|----------|
| dorm room fund | https://www.dormroomfund.com/apply |
| airbnb | https://boards-api.greenhouse.io/v1/boards/airbnb/jobs |
| affirm | https://boards-api.greenhouse.io/v1/boards/affirm/jobs |
| airtable | https://boards-api.greenhouse.io/v1/boards/airtable/jobs |
| anthropic | https://boards-api.greenhouse.io/v1/boards/anthropic/jobs |
| asana | https://boards-api.greenhouse.io/v1/boards/asana/jobs |
| brex | https://boards-api.greenhouse.io/v1/boards/brex/jobs |
| chime | https://boards-api.greenhouse.io/v1/boards/chime/jobs |
| cloudflare | https://boards-api.greenhouse.io/v1/boards/cloudflare/jobs |
| coinbase | https://boards-api.greenhouse.io/v1/boards/coinbase/jobs |
| cockroachlabs | https://boards-api.greenhouse.io/v1/boards/cockroachlabs/jobs |
| contentful | https://boards-api.greenhouse.io/v1/boards/contentful/jobs |
| datadog | https://boards-api.greenhouse.io/v1/boards/datadog/jobs |
| databricks | https://boards-api.greenhouse.io/v1/boards/databricks/jobs |
| discord | https://boards-api.greenhouse.io/v1/boards/discord/jobs |
| dropbox | https://boards-api.greenhouse.io/v1/boards/dropbox/jobs |
| duolingo | https://boards-api.greenhouse.io/v1/boards/duolingo/jobs |
| elastic | https://boards-api.greenhouse.io/v1/boards/elastic/jobs |
| figma | https://boards-api.greenhouse.io/v1/boards/figma/jobs |
| flexport | https://boards-api.greenhouse.io/v1/boards/flexport/jobs |
| gitlab | https://boards-api.greenhouse.io/v1/boards/gitlab/jobs |
| gusto | https://boards-api.greenhouse.io/v1/boards/gusto/jobs |
| hubspot | https://boards-api.greenhouse.io/v1/boards/hubspot/jobs |
| instacart | https://boards-api.greenhouse.io/v1/boards/instacart/jobs |
| linear | https://jobs.ashbyhq.com/linear |
| lyft | https://boards-api.greenhouse.io/v1/boards/lyft/jobs |
| netlify | https://boards-api.greenhouse.io/v1/boards/netlify/jobs |
| notion | https://jobs.ashbyhq.com/notion |
| openai safety fellowship | https://openai.com/index/introducing-openai-safety-fellowship/ |
| openai residency | https://openai.com/residency/ |
| pagerduty | https://boards-api.greenhouse.io/v1/boards/pagerduty/jobs |
| pinterest | https://boards-api.greenhouse.io/v1/boards/pinterest/jobs |
| postman | https://boards-api.greenhouse.io/v1/boards/postman/jobs |
| ramp | https://api.ashbyhq.com/posting-api/job-board/ramp |
| reddit | https://boards-api.greenhouse.io/v1/boards/reddit/jobs |
| retool | https://api.ashbyhq.com/posting-api/job-board/retool |
| revenuecat | https://jobs.ashbyhq.com/revenuecat |
| robinhood | https://boards-api.greenhouse.io/v1/boards/robinhood/jobs |
| sofi | https://boards-api.greenhouse.io/v1/boards/sofi/jobs |
| sentry | https://sentry.io/jobs/list.json |
| stripe | https://boards-api.greenhouse.io/v1/boards/stripe/jobs |
| supabase | https://api.ashbyhq.com/posting-api/job-board/supabase |
| tailscale | https://boards-api.greenhouse.io/v1/boards/tailscale/jobs |
| toast | https://boards-api.greenhouse.io/v1/boards/toast/jobs |
| twitch | https://boards-api.greenhouse.io/v1/boards/twitch/jobs |
| vercel | https://boards-api.greenhouse.io/v1/boards/vercel/jobs |
| ziprecruiter | https://boards-api.greenhouse.io/v1/boards/ziprecruiter/jobs |
| anthropic fellows program | https://alignment.anthropic.com/2025/anthropic-fellows-program-2026/ |
| anthropic ai safety fellow | https://www.anthropic.com/careers/jobs/5023394008 |
| anthropic ai security fellow | https://www.anthropic.com/careers/jobs/5030244008 |
| aws cloud credit for research | https://aws.amazon.com/research-credits/ |
| aws compute for climate fellowship | https://aws.amazon.com/startups/learn/compute-for-climate-fellowship?lang=en-US |
| google public policy fellowship | https://www.google.com/policyfellowship/ |
| google ai residency | https://research.google.com/teams/brain/residency/ |
| google cloud for researchers | https://cloud.google.com/edu/researchers |

## Government Programs

| Org | Endpoint |
|---------|----------|
| nsf career | https://www.nsf.gov/funding/opportunities/career-faculty-early-career-development-program |

## Nonprofit Organizations

| Org | Endpoint |
|---------|----------|
| american institute of physics grants | https://www.aip.org/grants |
| burroughs wellcome fund grants | https://www.bwfund.org/grants/ |
| chan zuckerberg initiative grants | https://chanzuckerberg.com/grants-ventures/grants/ |
| ford foundation grants | https://www.fordfoundation.org/work/our-grants/ |
| gates foundation grant opportunities | https://www.gatesfoundation.org/about/how-we-work/grant-opportunities |
| hhmi investigators | https://www.hhmi.org/programs/investigators |
| kavli foundation funding | https://www.kavlifoundation.org/funding |
| knight foundation funding | https://knightfoundation.org/how-we-fund/ |
| macarthur foundation grant guidelines | https://www.macfound.org/programs/field-support/impact-investments/grant-guidelines |
| mozilla open source support awards | https://www.mozilla.org/en-US/moss/ |
| national geographic funding opportunities | https://www.nationalgeographic.org/funding-opportunities/ |
| open society fellowships | https://www.opensocietyfoundations.org/grants |
| packard foundation grants | https://www.packard.org/grantees/search-our-grants/ |
| rockefeller foundation grants | https://www.rockefellerfoundation.org/grants/ |
| rwjf impact investing | https://www.rwjf.org/en/about-rwjf/impact-investing.html |
| simons foundation fellows-to-faculty | https://www.simonsfoundation.org/funding-opportunities/fellows-to-faculty/ |
| simons foundation funding | https://www.simonsfoundation.org/funding-opportunities/fellows-to-faculty/funding/ |
| sloan foundation apply | https://sloan.org/grants/apply |
| sloan research fellowships | https://apply.sloan.org/prog/2026_sloan_research_fellowships/ |
| spencer foundation training grants | https://www.spencer.org/training-grants |
| wellcome research career development fellowships | https://wellcome.org/funding/research-career-development-fellowships |
| wellcome international training fellowships | https://wellcome.org/funding/international-training-fellowships |
| wikimedia foundation grants | https://wikimediafoundation.org/what-we-do/ |

## Notes

- Treat nonprofit foundations, charities, and mission-driven institutes as first-class sources.
- For companies, it's okay to include general career or posting endpoints when no dedicated fellowship page exists.
- If a foundation page says a scheme is closed, keep it in the table if it is still a useful canonical reference, and mark it closed when answering the user.
