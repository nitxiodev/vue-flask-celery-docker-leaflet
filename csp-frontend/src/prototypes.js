String.prototype.capitalize = function() {
  return this.split(" ")
    .map(function(a) {
      return a.charAt(0).toUpperCase() + a.slice(1);
    })
    .join(" ");
};
