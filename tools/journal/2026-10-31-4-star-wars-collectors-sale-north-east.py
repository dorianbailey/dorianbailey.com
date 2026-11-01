"""Journal: The Star Wars sale."""
post(dict(
    date="2026-10-31", card_sub="Better Selling With Bailey &middot; May 2026",
    slug="star-wars-collectors-sale-north-east", section="Estate sales",
    title="A Star Wars Collector’s Sale in North East",
    seo="Star Wars Collector’s Sale in North East, PA | Better Selling With Bailey",
    desc="A Better Selling With Bailey sale in North East, Pennsylvania: a Star Wars collection of action figures, books and sealed LEGO sets that drew a crowd through the rain and the local news.",
    standfirst="In May 2026, a collection of action figures, books and sealed LEGO sets drew a line of buyers through heavy rain and wind, and the local news came out to film it.",
    dek="Action figures, books and sealed LEGO sets, a line of buyers in the rain, and a story on the local news.",
    head=jph(2), card_pos="center 35%",
    about=["Estate sales", "Star Wars collectibles", "North East, Pennsylvania"],
    body=f"""          <p class="article__lede">Some sales sell themselves once the right people hear about them. This one was a Star Wars collection in North East: boxed action figures by the hundred, books and sealed LEGO sets, staged across a garage and down the side of the house.</p>

          <h2>The setup</h2>
          <p>The garage was staged wall to wall, with boxed figures on racks and LEGO sets stacked where buyers could see the boxes. More tables ran down the side of the house under a canopy, which mattered once the rain came in.</p>
{jfig(jph(0), "The garage, staged")}
{jpair((jph(1), "Tables down the side of the house"), (jph(4), "Racks of boxed figures"))}

          <h2>Rain, and a crowd anyway</h2>
          <p><a href="{LINKS['erie']}" rel="noopener">YourErie.com reported</a> an eager crowd through heavy rain and wind. Buyers lined up on the wet sale morning and browsed the tables under the canopy.</p>
{jpair((jph(5), "Under the canopy"), (jph(3), "The local news, filming the sale"))}

          <h2>On the news</h2>
          <p>The local TV news came out to film the sale, and YourErie.com ran the story in May 2026.</p>

          <h2>What the clients said</h2>
          <blockquote class="quote">
            <p>Everything was done for me. Great turnout for the sale. Was better than I hoped for. The local TV station even came out and did a story on the sale.</p>
            <cite>Andy N., Google review</cite>
          </blockquote>
          <blockquote class="quote">
            <p>Ran a giant garage sale for me and it went off without a hitch. Great advertising and phenomenal work setting things up and execution of the sale.</p>
            <cite>Ben N., Google review</cite>
          </blockquote>

          <h2>Why it worked</h2>
          <p>A collection sells when it&rsquo;s laid out so buyers can take it in at a glance, and promoted to the people who collect it. Staging, promotion and running the floor are the whole job; <a href="../how-estate-sales-work-erie-county/">here is how a sale works</a>, step by step.</p>
          <p class="article__credit">Photographs of the sale by clients Ben and Andy Nagle, from their Google reviews.</p>
{cta("Book an estate sale", "Have a collection, a garage or a whole house to sell? Pick a date and I&rsquo;ll reply to set up a walkthrough.", [BOOK_ESTATE, EMAIL_BSWB])}""",
    particulars=[("Where", "North East, Pennsylvania"), ("When", "May 2026"),
                 ("Collection", "Star Wars action figures, books and sealed LEGO sets"),
                 ("Press", f'<a href="{LINKS["erie"]}" rel="noopener">YourErie.com, May 2026</a>'),
                 ("Company", f'<a href="{J}better-selling/">Better Selling With Bailey</a>'),
                 ("Photographs", "Ben and Andy Nagle")],
    images=[jph(i) for i in (2, 0, 1, 4, 5, 3)],
))
