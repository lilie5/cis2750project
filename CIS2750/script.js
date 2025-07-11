$(document).ready(function() {
    var draw = false;
    var interval = 100; //interval 100
    var SVGs = $('#svgContainer div').length; //get the length of our svg container
    var currIndex = 0; //current index
    $('#svgContainer div').hide().first().show(); //show the first svg container


    $(document).mousemove(function(event) {
        if (draw == true) {
            drawLine(event);
        }
    });

    $(document).mousedown(function(event) {
        $('#line').show();
        draw = true;
        drawLine(event);
    });

    $(document).mouseup(function(event) {
        event.preventDefault(); // Prevent default form submission
        
        if (draw == true) {
            var mx = event.pageX * 2 - 25;
            var my = event.pageY * 2 - 25;
            var cx = parseFloat($('#cueball').attr('cx'));
            var cy = parseFloat($('#cueball').attr('cy'));
            $.ajax({
                url: '/submit',
                type: 'POST',
                contentType: 'application/json',
                data: JSON.stringify({
                    mouseX: mx,
                    mouseY: my,
                    ballCenterX: cx,
                    ballCenterY: cy
                }),
                success: function(response) {
                    window.location.href = 'animate.html';
                   // window.location.href = 'display.html?animate=true';

                },
                error: function(error) {
                    console.error('ERR: ', error);
                }
            });
            $('#line').hide(); 
        }
        draw = false;
    });

    function displaySVGs() {
        currIndex += 1;
        if (SVGs <= currIndex) {
            clearInterval(animationTimer); 
            if (temp == null) {
                if (window.location.pathname.endsWith('animate.html')) {
                    if (temp == null) {
                        var temp = $('#svgContainer div').eq(currIndex - 1);
                        var htmlTemp = temp.html();
                        $.ajax({
                            url: '/second',
                            type: 'POST',
                            contentType: 'application/json',
                            data: JSON.stringify({
                                new_svg: htmlTemp
                            }),
                            success: function(response) {
                                window.location.href = 'second.html';
                            },
                            error: function(error) {
                                console.error('Error processing shot:', error);
                            }
                        });
                    }
                }
            }
            return;
        }
        $('#svgContainer div').hide();
        $('#svgContainer div').eq(currIndex).show();
    }

    animationTimer = setInterval(displaySVGs, interval);
    function drawLine(event) {
        var bx = parseFloat($('#cueball').attr('cx'));
        var by = parseFloat($('#cueball').attr('cy'));
        $('#line').attr({
            'x1': bx,
            'y1': by,
            'x2': event.pageX * 2 - 25,
            'y2': event.pageY * 2 - 25
        });
    }
    
});