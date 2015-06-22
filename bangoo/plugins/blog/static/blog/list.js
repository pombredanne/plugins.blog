angular.module('bangoo.blog.list', ['codehouse.ui'], function($interpolateProvider) {
    $interpolateProvider.startSymbol('[[');
    $interpolateProvider.endSymbol(']]');
})
.controller('BangooBlogListController', ['$http', '$element', '$scope', function($http, $element, $scope){
    var self = this;
    this.listUrl = $element.data('url');
    this.publishUrl = $element.data('publish');

    this.posts = [];
    $http.get(this.listUrl).success(function(data){
        self.posts = data;
    });

    var insert = function(post){
        for(var i=0; i<self.posts.length; i++){
            var p = self.posts[i];
            if(p.id == post.id){
                self.posts[i] = post;
                return
            }
        }
    };

    this.publish = function(id, e){
        var elem = $(e.target);
        elem.attr('disabled', true);

        $http({
            method: 'POST',
            url: self.publishUrl,
            data: {id: id, state: 'publish'},
            xsrfHeaderName: 'X-CSRFToken',
            xsrfCookieName: 'csrftoken'
        }).success(function(data){
            $('.top-right').notify({
                type: 'success',
                message: { text: 'Published successfully!' },
                fadeOut: { enabled: true, delay: 5000 }
            }).show();
            elem.attr('disabled', false);
            insert(data)
        }).error(function(retval, status, headers, config){
            $('.top-right').notify({
                type: 'danger',
                message: {text: 'Unexpected error happened!'},
                fadeOut: {enabled: true, delay: 5000}
            }).show();
            elem.attr('disabled', false);
        });
    }
}]);