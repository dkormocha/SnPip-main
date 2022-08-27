$(document).ready(function(){           // function to download stat tables separately 
  $('#export').click(function() {
    var titles = [];
    var data = [];

 
    $('#my_id th').each(function() {      // finds any item with id my_id and then the th attribute and pushes the content
      titles.push($(this).text());
    });


    $('#my_id td').each(function() {    // finds any item with id my_id and then the td attribute and pushes the content
      data.push($(this).text());
    });
    

    var CSVString = prepCSVRow(titles, titles.length, '');    // csv string
    CSVString = prepCSVRow(data, titles.length, CSVString);


    var downloadLink = document.createElement("a"); //creates a csv file dynamically 
    var blob = new Blob(["\ufeff", CSVString]);
    var url = URL.createObjectURL(blob);
    downloadLink.href = url;
    downloadLink.download = "Hudson_FST.tsv";


    document.body.appendChild(downloadLink);  //download link created 
    downloadLink.click();
    document.body.removeChild(downloadLink);
  });


  function prepCSVRow(arr, columnCount, initial) {    // takes the table data from html and formats it for csv download
    var row = ''; 
    var delimeter = ','; 
    var newLine = '\r\n'; 

 
    function splitArray(_arr, _count) {
      var splitted = [];
      var result = [];
      _arr.forEach(function(item, idx) {
        if ((idx + 1) % _count === 0) {
          splitted.push(item);
          result.push(splitted);
          splitted = [];
        } else {
          splitted.push(item);
        }
      });
      return result;
    }
    var plainArr = splitArray(arr, columnCount);

    plainArr.forEach(function(arrItem) {
      arrItem.forEach(function(item, idx) {
        row += item + ((idx + 1) === arrItem.length ? '' : delimeter);
      });
      row += newLine;
    });
    return initial + row;
  }
});



$(document).ready(function(){             // same function but for different stat table
  $('#export1').click(function() {
    var titles = [];
    var data = [];


    $('#my_id1 th').each(function() {
      titles.push($(this).text());
    });


    $('#my_id1 td').each(function() {
      data.push($(this).text());
    });
    

    var CSVString = prepCSVRow(titles, titles.length, '');
    CSVString = prepCSVRow(data, titles.length, CSVString);

 
    var downloadLink = document.createElement("a");
    var blob = new Blob(["\ufeff", CSVString]);
    var url = URL.createObjectURL(blob);
    downloadLink.href = url;
    downloadLink.download = "Shannon_Diversity.tsv";


    document.body.appendChild(downloadLink);
    downloadLink.click();
    document.body.removeChild(downloadLink);
  });


  function prepCSVRow(arr, columnCount, initial) {
    var row = ''; 
    var delimeter = ','; 
    var newLine = '\r\n'; 



    function splitArray(_arr, _count) {
      var splitted = [];
      var result = [];
      _arr.forEach(function(item, idx) {
        if ((idx + 1) % _count === 0) {
          splitted.push(item);
          result.push(splitted);
          splitted = [];
        } else {
          splitted.push(item);
        }
      });
      return result;
    }
    var plainArr = splitArray(arr, columnCount);

    plainArr.forEach(function(arrItem) {
      arrItem.forEach(function(item, idx) {
        row += item + ((idx + 1) === arrItem.length ? '' : delimeter);
      });
      row += newLine;
    });
    return initial + row;
  }
});




$(document).ready(function(){
  $('#export2').click(function() {
    var titles = [];
    var data = [];


    $('#my_id2 th').each(function() {
      titles.push($(this).text());
    });


    $('#my_id2 td').each(function() {
      data.push($(this).text());
    });

    var CSVString = prepCSVRow(titles, titles.length, '');
    CSVString = prepCSVRow(data, titles.length, CSVString);


    var downloadLink = document.createElement("a");
    var blob = new Blob(["\ufeff", CSVString]);
    var url = URL.createObjectURL(blob);
    downloadLink.href = url;
    downloadLink.download = "Tajima_D.tsv";


    document.body.appendChild(downloadLink);
    downloadLink.click();
    document.body.removeChild(downloadLink);
  });


  function prepCSVRow(arr, columnCount, initial) {
    var row = ''; 
    var delimeter = ','; 
    var newLine = '\r\n'; 


    function splitArray(_arr, _count) {
      var splitted = [];
      var result = [];
      _arr.forEach(function(item, idx) {
        if ((idx + 1) % _count === 0) {
          splitted.push(item);
          result.push(splitted);
          splitted = [];
        } else {
          splitted.push(item);
        }
      });
      return result;
    }
    var plainArr = splitArray(arr, columnCount);

    plainArr.forEach(function(arrItem) {
      arrItem.forEach(function(item, idx) {
        row += item + ((idx + 1) === arrItem.length ? '' : delimeter);
      });
      row += newLine;
    });
    return initial + row;
  }
});



$(document).ready(function(){
  $('#export3').click(function() {
    var titles = [];
    var data = [];


    $('#my_id3 th').each(function() {
      titles.push($(this).text());
    });


    $('#my_id3 td').each(function() {
      data.push($(this).text());
    });

    var CSVString = prepCSVRow(titles, titles.length, '');
    CSVString = prepCSVRow(data, titles.length, CSVString);


    var downloadLink = document.createElement("a");
    var blob = new Blob(["\ufeff", CSVString]);
    var url = URL.createObjectURL(blob);
    downloadLink.href = url;
    downloadLink.download = "HaplotypeD.tsv";


    document.body.appendChild(downloadLink);
    downloadLink.click();
    document.body.removeChild(downloadLink);
  });


  function prepCSVRow(arr, columnCount, initial) {
    var row = ''; 
    var delimeter = ','; 
    var newLine = '\r\n'; 


    function splitArray(_arr, _count) {
      var splitted = [];
      var result = [];
      _arr.forEach(function(item, idx) {
        if ((idx + 1) % _count === 0) {
          splitted.push(item);
          result.push(splitted);
          splitted = [];
        } else {
          splitted.push(item);
        }
      });
      return result;
    }
    var plainArr = splitArray(arr, columnCount);

    plainArr.forEach(function(arrItem) {
      arrItem.forEach(function(item, idx) {
        row += item + ((idx + 1) === arrItem.length ? '' : delimeter);
      });
      row += newLine;
    });
    return initial + row;
  }
});