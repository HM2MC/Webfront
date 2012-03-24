// Setup for the pages

$(function(){
    // set min-height of container, attach newscounter
    $('#container').css('min-height',$(window).height()-25);
    $(window).resize(function(){
        $('#container').css('min-height',$(window).height()-25)
    });
    
    // hide login extras until mouseover
    $('#loginner').hover(
    	function(){
    		$(this).children('.hidden').toggle('medium');
    	}, 
    	function(){
    		$(this).children('.hidden').toggle('medium');
    	});
    
    
    // move params around
    $('#searchParams').css('left',function(index,value){
                $(this).width(function(){
                    return 15 + Math.max.apply(Math, $('#searchParams select').map(function(){ return $(this).width(); }).get());
                });
                // gets rid of ugly whitespace below the options bar
                $(this).css('marginBottom',function(){
                    return 0 - $(this).height();
                });
                return -31 - parseInt($(this).width());
            }).css('visibility','visible');
    
    
    
	//alert($('#searchParams').css('left'));
    	
    // move, replace searchbar stuff with images
    $('#searchbarActual').prepend($('ul#modifiers'));
    $('ul#modifiers li a').html(function(){
        return "<img src='/media/images/"+$(this).attr('id')+".png'/>"
    });
    
    $('#wrapper').width(function(){
    	w = $('#container').outerWidth()
    	final = w + $('#searchParams').outerWidth();
    	//alert(w);
    	//alert(final);
    	return w;//final;
    });/**/ 
    $('#wrapper').css('padding-left', function(){
    	return $('#searchParams').outerWidth();
    });
    
    /*#('#container').css('margin-left',function(index, value){
    //	alert($('#searchParams').css('left'));
    	return "138px";//$('#searchParams').css('left');
    });/**/
    // move subset lists out of navbar
    $('#subsetHold').prepend($('ul#subset'));
    
    // make navbar opaque, prettily
    $(window).scroll(function(){
        if($(window).scrollTop() > 350){
            $('#sitewide').css('backgroundColor','rgba(70, 130, 180,1)');
        } else if ($(window).scrollTop() == 0){
            $('#sitewide').css('backgroundColor','rgba(70, 130, 180,0.5)'); 
        } else {
            $('#sitewide').css('backgroundColor','rgba(70, 130, 180,'+(0.5+$(window).scrollTop()/700)+')');
        }
    });
    
    
});