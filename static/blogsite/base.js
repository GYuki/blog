var app = angular.module('BlogApp', []);

app.controller('BaseController', function($scope, $http) {
  $scope.notification = 0
  $http({
    url: "/blogs/fresh_posts/",
    method: "GET"
  }).then(function (response) {
    $scope.notification = response.data.len
  })
}
)
