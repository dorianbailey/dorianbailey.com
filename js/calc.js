// Better Selling With Bailey: "What would I keep?"
// Payout = total sales - 20% commission - $995 flat fee (the published standard terms).
(function () {
  var root = document.querySelector('[data-calc]');
  if (!root) return;
  var fee = Number(root.getAttribute('data-fee'));
  var rate = Number(root.getAttribute('data-rate'));
  var num = root.querySelector('#calc-total');
  var range = root.querySelector('[data-calc-range]');
  var out = function (k) { return root.querySelector('[data-calc-out="' + k + '"]'); };
  var money = new Intl.NumberFormat('en-US', { style: 'currency', currency: 'USD', maximumFractionDigits: 0 });
  var breakEven = Math.ceil(fee / (1 - rate));
  var defaultNote = out('note').textContent;

  function render(total, from) {
    total = Math.max(0, Math.round(Number(total) || 0));
    if (from !== 'num') num.value = total;
    if (from !== 'range') range.value = Math.min(Math.max(total, Number(range.min)), Number(range.max));
    var commission = total * rate;
    var keep = total - commission - fee;
    out('total').textContent = money.format(total);
    out('commission').textContent = '−' + money.format(commission);
    out('keep').textContent = keep > 0 ? money.format(keep) : money.format(0);
    out('note').textContent = keep > 0
      ? defaultNote
      : 'Below about ' + money.format(breakEven) + ' in sales, the flat fee would outweigh the proceeds. Get in touch and we can talk through whether a sale makes sense.';
  }

  num.addEventListener('input', function () { render(num.value, 'num'); });
  range.addEventListener('input', function () { render(range.value, 'range'); });
  root.querySelectorAll('[data-calc-preset]').forEach(function (b) {
    b.addEventListener('click', function () { render(b.getAttribute('data-calc-preset')); });
  });
  render(num.value);
})();
