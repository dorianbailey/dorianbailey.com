"""Journal: Estate sale or garage sale."""
_rows = "".join(f"<tr><td>${t:,}</td><td>&minus;${round(t * 0.2):,}</td><td>&minus;$995</td><td>${t - round(t * 0.2) - 995:,}</td></tr>" for t in (3000, 8000, 16000))
_vs = [("Who runs it", "You, and whoever you can recruit", "A company, from pricing to cleanup"),
       ("What&rsquo;s for sale", "The extras, a few tables&rsquo; worth", "A house, a garage, a basement or a collection"),
       ("Pricing", "Stickers on the morning, haggling all day", "Priced before the doors open"),
       ("Setup", "Tables in the driveway", "Rooms staged so buyers can browse"),
       ("Promotion", "Signs and a post or two", "Listings, Facebook events and local outreach"),
       ("Sale days", "You work the table", "Staffed for you; you needn&rsquo;t be there"),
       ("Leftovers", "Yours to haul or donate", "Removed (free with Better Selling With Bailey)"),
       ("Cost", "Your time", "A fee, a commission, or both")]
_vsrows = "".join(f"<tr><th scope=\"row\">{a}</th><td>{b}</td><td>{c}</td></tr>" for a, b, c in _vs)
post(dict(
    date="2026-11-20", card_sub="An honest comparison, side by side",
    slug="estate-sale-vs-garage-sale", section="Estate sales",
    title="Estate Sale or Garage Sale: Which One You Need",
    seo="Estate Sale vs. Garage Sale: Which Is Right? | Dorian Bailey",
    desc="Estate sale vs. garage sale: who runs it, pricing, staging, promotion and cost compared honestly, and when a garage sale is the better choice in Erie County.",
    standfirst="Who does the work, who sets the prices, who brings the buyers and what it costs, and the cases where running it yourself is the smarter choice.",
    dek="Scale, pricing, staging, promotion and cost, side by side, and an honest answer to when a garage sale is the better choice.",
    head=jph(4), card_pos="50% center",
    about=["Estate sales", "Garage sales", "Erie County, Pennsylvania"],
    body=f"""          <p class="article__lede">An estate sale and a garage sale both put a household&rsquo;s things in front of buyers, but they aren&rsquo;t the same job. A garage sale is you, a driveway and a weekend, selling what you don&rsquo;t need. An estate sale sells the contents of a home, or a garage, basement or collection, and someone else prices, stages, promotes and runs it. Here is an honest comparison of an estate sale vs. a garage sale, including when the garage sale is the better choice.</p>

          <h2>Estate sale vs. garage sale at a glance</h2>
          <div class="article__table article__table--text">
            <table>
              <thead><tr><td></td><th scope="col">Garage sale</th><th scope="col">Estate sale</th></tr></thead>
              <tbody>{_vsrows}</tbody>
            </table>
          </div>

          <h2>Who does the work</h2>
          <p>A garage sale is yours from start to finish. You sort, price and set up before the early buyers arrive, then sit at the table all day making change and fielding offers. At the end you pack up what didn&rsquo;t sell and find somewhere for it to go.</p>
          <p>An estate sale hands that work to someone else. With Better Selling With Bailey it starts with a walkthrough, where I look at everything that&rsquo;s going and price it, with you as involved as you like. Then come staging, promotion, the sale days, where I run the floor, and cleanup. You don&rsquo;t need to be there. <a href="https://checkbook.org/national/getting-rid-of-your-unwanted-stuff/articles/Estate-Sales-5858" rel="noopener">Consumers&rsquo; Checkbook</a>, a nonprofit consumer guide, notes that estate sales usually run two or three days.</p>

          <h2>Pricing, staging and promotion</h2>
          <p>Garage sale buyers come for bargains, and garage sale prices are set to match: round numbers, quick decisions, a lot of haggling. That suits everyday household things. It sells a valuable piece short when nobody has looked at what it is.</p>
          <p>At an estate sale, everything is priced before the doors open, rooms are staged so buyers can browse and find what they came for, and the sale is promoted through listings, Facebook events and local outreach. Promotion matters most for collections, because the buyers who&rsquo;ll pay fairly for them are collectors, and collectors have to hear about the sale to come.</p>
          <p>If you run your own sale, call your borough, township or city office before you put up signs, and ask whether you need a permit and where signs are allowed.</p>

          <h2>What each one costs</h2>
          <p>A garage sale keeps every dollar; what it costs is your time. An estate sale costs a share of the proceeds. Consumers&rsquo; Checkbook reports that liquidators typically keep 30 to 50 percent, often with a minimum. My terms are a $995 flat fee plus 20% of total sales, agreed before the sale, with whatever is left removed at no charge. Here is the math at three totals:</p>
          <div class="article__table">
            <table>
              <thead><tr><th scope="col">Total sales</th><th scope="col">Commission, 20%</th><th scope="col">Flat fee</th><th scope="col">You keep</th></tr></thead>
              <tbody>{_rows}</tbody>
            </table>
          </div>
          <p>Look at the first row. On a small sale, the flat fee is a large share of the total, and that is the honest case for doing it yourself. Try your own number in <a href="{J}better-selling/#calc-title">the calculator</a>.</p>

          <h2>When a garage sale is the better choice</h2>
          <ul>
            <li><strong>It&rsquo;s a few tables of extras</strong>, not a houseful.</li>
            <li><strong>You&rsquo;re staying in the house</strong> and there&rsquo;s no deadline.</li>
            <li><strong>Most of it is everyday</strong>: kids&rsquo; clothes, dishes, a lamp or two, priced in single dollars.</li>
            <li><strong>You have the weekend</strong>, and you don&rsquo;t mind spending it at a folding table.</li>
            <li><strong>You have a plan for the leftovers</strong>, whether a donation drop-off or a friend with a truck.</li>
          </ul>
          <p>If that&rsquo;s you, run the garage sale yourself. On a sale that size, any fee takes too large a share.</p>

          <h2>When an estate sale makes more sense</h2>
          <ul>
            <li><strong>A whole house</strong>, or a garage, basement or collection that has outgrown a few tables.</li>
            <li><strong>A deadline</strong>, such as a closing date or a move.</li>
            <li><strong>You can&rsquo;t be there</strong>, or would rather not be.</li>
            <li><strong>A collection</strong> that sells best when it&rsquo;s shown to collectors: toys and LEGO, video games, sports cards, trading cards.</li>
            <li><strong>You want it gone afterward</strong>, without a second weekend of hauling.</li>
          </ul>
          <p>The line between the two isn&rsquo;t always sharp. Many clients treat a sale as a cleanout of a garage, basement or collection that happens to pay. A client&rsquo;s Google review of [[star-wars-collectors-sale-north-east|a collector&rsquo;s sale in North East]] put it this way:</p>
          <blockquote class="quote">
            <p>Ran a giant garage sale for me and it went off without a hitch. Great advertising and phenomenal work setting things up and execution of the sale.</p>
            <cite>Ben N., Google review</cite>
          </blockquote>
          <p>If an estate sale sounds right, [[prepare-home-for-estate-sale|getting your home ready]] covers what to set aside first, and [[how-estate-sales-work-erie-county|how an estate sale works]] covers the rest. <a href="{J}better-selling/">Better Selling With Bailey</a> runs sales in clients&rsquo; homes across Erie County.</p>
          <p class="article__credit">Photograph of that sale by clients Ben and Andy Nagle, from their Google reviews.</p>
{cta("Book an estate sale", "Not sure which you need? Pick a date and I&rsquo;ll reply to set up a walkthrough, and give you a straight answer.", [BOOK_ESTATE, EMAIL_BSWB])}""",
    particulars=[("Company", f'<a href="{J}better-selling/">Better Selling With Bailey</a>'), ("Region", "Erie County, Pennsylvania"),
                 ("Terms", "$995 flat fee plus 20% commission; leftover removal free"),
                 ("Email", f'<a href="mailto:{BSWB_EMAIL}">{BSWB_EMAIL}</a>'), ("Photograph", "Ben and Andy Nagle")],
    images=[jph(4)],
))
