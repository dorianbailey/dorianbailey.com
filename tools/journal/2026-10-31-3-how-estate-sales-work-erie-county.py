"""Journal: How an estate sale works."""
_rows = "".join(f"<tr><td>${t:,}</td><td>&minus;${round(t * 0.2):,}</td><td>&minus;$995</td><td>${t - round(t * 0.2) - 995:,}</td></tr>" for t in (10000, 16000))
post(dict(
    date="2026-10-31", card_sub="Better Selling With Bailey, start to finish",
    slug="how-estate-sales-work-erie-county", section="Estate sales",
    title="How an Estate Sale Works in Erie County",
    seo="How an Estate Sale Works in Erie County, PA | Dorian Bailey",
    desc="How Better Selling With Bailey runs an estate sale in Erie County, PA: walkthrough and pricing, staging, promotion, sale days, cleanup and what you keep, explained by Dorian Bailey.",
    standfirst="From the first walkthrough to the last box out the door: what happens, what it costs, and what you keep.",
    dek="Walkthrough, pricing, staging, promotion, sale days and cleanup, with the fees worked out: an estate sale with Better Selling With Bailey, start to finish.",
    head=jph(5), card_pos="center 40%",
    about=["Estate sales", "Erie County, Pennsylvania", "Better Selling With Bailey"],
    body=f"""          <p class="article__lede">An estate sale is a sale of a home&rsquo;s contents, held in the home itself. It isn&rsquo;t only for after a loss: people hold them when they move or downsize, and many of my clients treat a sale as a cleanout of a garage, basement or collection that happens to pay. Here is how a sale works with Better Selling With Bailey, start to finish.</p>

          <h2>Six steps</h2>
          <ol class="article__steps">
            <li><strong>Walkthrough and pricing.</strong> I walk through the home with you, assess everything to be sold and price it to sell. You can be involved in every pricing decision or none of them. Before the walkthrough, set aside anything you&rsquo;re keeping: family photographs, papers, and anything with sentimental value.</li>
            <li><strong>Staging.</strong> Rooms are organized and merchandise is laid out so buyers can browse easily and find what they came for. When a sale outgrows the house, tables go outside under a canopy.</li>
            <li><strong>Promotion.</strong> Listings, Facebook events and local outreach bring the right buyers to the door, whatever the weather.</li>
            <li><strong>Sale days.</strong> I run the floor: every customer, every sale and every question.</li>
            <li><strong>Cleanup.</strong> Teardown at the end of the sale, and free removal of whatever is left if you want it gone.</li>
            <li><strong>Proceeds.</strong> The earnings go to you, minus the flat fee and commission agreed before the sale began.</li>
          </ol>

          <h2>What it costs</h2>
          <p>The terms are simple: a $995 flat fee plus 20% of total sales, agreed before the sale begins. Removing whatever is left afterward is free. Here is the math on two sale totals:</p>
          <div class="article__table">
            <table>
              <thead><tr><th scope="col">Total sales</th><th scope="col">Commission, 20%</th><th scope="col">Flat fee</th><th scope="col">You keep</th></tr></thead>
              <tbody>{_rows}</tbody>
            </table>
          </div>
          <p>The best weekend so far brought in more than $16,000. To try your own number, use <a href="{J}better-selling/#calc-title">the calculator on the Better Selling With Bailey page</a>.</p>

          <h2>What sells</h2>
          <p>These are the categories that consistently draw buyers at Erie County sales:</p>
          <ul class="article__cols">
{chr(10).join(f"            <li>{x}</li>" for x in SELLS)}
          </ul>
          <p>Collections do especially well when they&rsquo;re promoted to the people who collect them, as at <a href="../star-wars-collectors-sale-north-east/">a Star Wars collector&rsquo;s sale in North East</a> in May 2026.</p>

          <h2>Do you need to be there?</h2>
          <p>No. Some clients like to be on hand for every minute; others would rather hand everything over and come back when it&rsquo;s done. Either works.</p>

          <h2>Where</h2>
          <p>Better Selling With Bailey is based in North East and runs sales in clients&rsquo; homes across Erie County, including Erie.</p>
{cta("Book an estate sale", "Pick a date and I&rsquo;ll reply to set up a walkthrough.", [BOOK_ESTATE, EMAIL_BSWB])}""",
    particulars=[("Company", f'<a href="{J}better-selling/">Better Selling With Bailey</a>'), ("Region", "Erie County, Pennsylvania"),
                 ("Terms", "$995 flat fee plus 20% commission; leftover removal free"),
                 ("Email", f'<a href="mailto:{BSWB_EMAIL}">{BSWB_EMAIL}</a>'), ("Photograph", "Ben and Andy Nagle")],
    images=[jph(5)],
))
