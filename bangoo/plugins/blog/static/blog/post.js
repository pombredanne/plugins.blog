angular.module('bangoo.blog.post', ['codehouse.ui'], function($interpolateProvider) {
    $interpolateProvider.startSymbol('[[');
    $interpolateProvider.endSymbol(']]');
})
.controller('BangooBlogPostController', ['$http', '$element', '$scope', function($http, $element, $scope){
    var self = this;
    this.url = $element.data('url');

    $scope.data = {};
    $scope.errors = {};

    $http.get(this.url).success(function(data){
        $scope.data = data;
    });

    var setState = function(data){
        $element.attr('url', data.url);
        self.url = data.url;
        delete data.url;

        if($scope.data.id === undefined){
            var pathParts = window.location.pathname.split('/');
            pathParts[pathParts.indexOf('new')] = data.id;
            window.history.replaceState({}, '', pathParts.join('/'));
        }
    };

    this.toFormData = function(obj){
        var fd = new FormData();
        var keys = Object.keys(obj);
        for(var i=0; i<keys.length; i++){
            var key = keys[i];
            var value = obj[key];
            if(value && value.type !== undefined && value.type === 'file'){
                fd.append(key, value.files[0]);
                value.value = '';
            }
            else {
                fd.append(key, value===null?'':value);
            }
        }
        return fd
    };

    this.submit = function(postState, e){
        var elem = $(e.target);
        var data = $scope.data;
        data.state = postState;

        elem.attr('disabled', true);

        $http({
            method: 'POST',
            url: self.url,
            data: self.toFormData(data),
            xsrfHeaderName: 'X-CSRFToken',
            xsrfCookieName: 'csrftoken',
            headers : {'Content-Type' : undefined}
        }).success(function(data){
            $('.top-right').notify({
                type: 'success',
                message: { text: 'Content updated!' },
                fadeOut: { enabled: true, delay: 5000 }
            }).show();
            setState(data);
            $scope.data = data;
            $scope.errors = {};
            elem.attr('disabled', false);
        }).error(function(retval, status, headers, config){
            if(status !== 500){
                $scope.errors = retval;
                elem.attr('disabled', false);
            }
            else {
                $('.top-right').notify({
                    type: 'danger',
                    message: {text: 'Unexpected error happened!'},
                    fadeOut: {enabled: true, delay: 5000}
                }).show();
                elem.attr('disabled', false);
            }
        });
    }
}]);