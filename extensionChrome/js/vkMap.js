// (function($) {


//   $.fn.vkMap = function() {
    
//   }
//   // $.fn.vchrome = function(method) {
//   //     if (methods[method]) {
//   //         return this.each(methods[method]);
//   //     } else {
//   //         $.error("Method " +  method + " doesn't exist on jQuery.vchrome");
//   //     }
//   // };
// })(jQuery);

var createDot = function() {
  
}

$(document).ready(function() {
  $("#page_body").bind("DOMSubtreeModified", function() {
    $('.audio_row').each(createDot);
  });
});