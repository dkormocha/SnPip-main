$(document).ready(function(){
  $('#download').click(function ()
  {
    var retContent = [];
    var retString = '';
    $('table tr').each(function (idx, elem)
    {
      var elemText = [];
      $(elem).children('th,td').each(function (childIdx, childElem)
      {
        elemText.push($(childElem).text());
      });
      retContent.push(`${elemText.join(',\t')}`);
    });
    retString = retContent.join('\r\n');
    var file = new Blob([retString], {type: 'text/plain'});
    var btn = $('#download');
    btn.attr("href", URL.createObjectURL(file));
    btn.prop("download", "SNP_summary.tsv");
  });
});
