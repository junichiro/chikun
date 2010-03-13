(function(){
    window.Chikun = {};

    window.Chikun.Stage = function(hash)
    {
	this.stage = hash.stage;
	this.size = hash.size;

	this._init();
    };

    window.Chikun.Stage.prototype._init = function()
    {
    var alphabets = "abcdefghijklnmopqrstuvwxyz".split("");
    
	this.table = $("<table/>");
	this.cells = [];
	
	for( var i = 0 ; i < this.size ; i ++)
	{
	    var tr = $("<tr/>");
		this.cells[i] = [];
		
	    for( var j = 0 ; j < this.size ; j ++)
	    {
		var td = $("<td/>");
		var span = $("<span/>");
		if( i== 0 && j == 0 )
		{
		span.text("┌");
		}else if( i== 0 && j < this.size - 1)
		{
		    span.text("┬");
		}else if(i==0)
		{
		span.text("┐");
	    }else if( j == 0 && i < this.size - 1)
	    {
	    span.text("├");
	    }else if( j == this.size -1 && i < this.size - 1 )
	    {
	    span.text("┤");
	    }else if( j == 0 && i == this.size - 1)
	    {
	    span.text("└");
	    }else if( j == this.size -1 && i == this.size - 1)
	    {
	    span.text("┘");
	    }else if( i == this.size -1 )
	    {
	    span.text("┴");
	    }else
	    {
	    span.text("┼");
	    }
		span.attr("title" , alphabets[j] + alphabets[i] );
		span.click( function(){
			location.href = location.href + "/" + $(this).attr("title");
		} );
		
		td.append( span );
		tr.append( td );
		
		this.cells[i][j] = td;
		
	    }
	    this.table.append( tr ) ;
	    
	    this.alphabets = alphabets;
	}

	this.stage.append( this.table );

     };

	window.Chikun.Stage.prototype.puts = function(action)
	{
		var pos = action.position.split("");
		var j = this.alphabets.indexOf(pos[0]);
		var i = this.alphabets.indexOf(pos[1]);
		
		$("span" , this.cells[i][j]).remove();
		
		var stone = new Chikun.Stone( action.stone );
		this.cells[i][j].append( stone.span );
	};

     window.Chikun.Stone = function( color )
     {
		var span = $("<span/>");
		if( color == "black")
		{
			span.text("●");
		}else
		{
			span.text("○");
		}
		this.span = span;
     }

})();
