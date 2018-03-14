<?php
     session_start();
?>

<!DOCTYPE html>
<html>
<head>
	<title>Register</title>
	<link rel="stylesheet" href="https://maxcdn.bootstrapcdn.com/bootstrap/3.3.7/css/bootstrap.min.css">
	<script src="https://ajax.googleapis.com/ajax/libs/jquery/3.2.1/jquery.min.js"></script>
        <link rel="icon" href="Penguins.jpg">
        <link rel="stylesheet" type="text/css" href="https://maxcdn.bootstrapcdn.com/font-awesome/4.7.0/css/font-awesome.min.css">
	<script src="https://maxcdn.bootstrapcdn.com/bootstrap/3.3.7/js/bootstrap.min.js"></script>
	<link rel="stylesheet" href="//fonts.googleapis.com/css?family=Open+Sans:300,400,600,700&amp;lang=en" />
	<link rel="stylesheet" type="text/css" href="style.css" />
	<style>
	.fileuploader{
		width:400px;
		height:200px;
		margin: 60px auto 0px auto;
		background=color:#FFF;
		border: 1px solid #CCC;
		padding :6px;
	}
        </style>
</head>
<body>

<nav class="navbar navbar-inverse">
    <div class="container-fluid">
	<div class="navbar-header">
		<button type="button" class="navbar-toggle" data-toggle="collapse" data-target="#topNavBar">
			 <span class="icon-bar"></span>
			 <span class="icon-bar"></span>
			 <span class="icon-bar"></span>
		</button>
		<a class="navbar-brand" href="index.html">CoolPics</a>
	</div>
	
    <!-- items -->
	<div class="collapse navbar-collapse" id="topNavBar">
		
		<ul class="nav navbar-nav">
			<li class="active">
				<a href="pics.php">	
					<span class="glyphicon glyphicon-th-large" aria-hidden="true"></span>&nbsp;
					Pics
				</a>
			</li>
		</ul>

		<form class="navbar-form navbar-left" role="search" method="get" action="search.php">
			<div class="form-group">
				<input type="text" class="form-control" name="q" placeholder="Images by Username">
			</div>
			<button type="submit" class="btn btn-default">Search</button>
		
		</form>

		<ul class="nav navbar-nav navbar-right">
			<li class="">
                               <a href="https://github.com/arindam-modak" style="text-decoration:none;"><i class="fa fa-github" aria-hidden="true"></i> ADM</a>
                        </li>
			<li class="">
				<a href="addpic.php">	
					<span class="glyphicon glyphicon-plus" aria-hidden="true"></span>&nbsp;
					Add Pic
				</a>
			</li>
                        <li class="">
				<a href="FileUpload.php">	
					<span class="glyphicon glyphicon-plus" aria-hidden="true"></span>&nbsp;
					Upload Pic
				</a>
			</li>
                        <li class="">
				<a href="register.php">	
					<span class="glyphicon glyphicon-th-large" aria-hidden="true"></span>&nbsp;
					Register
				</a>
			</li>
                        <li class="">
				<a href="login.php">	
					<span class="glyphicon glyphicon-user" aria-hidden="true"></span>&nbsp;
					login
				</a>
			</li>
			<li class="">
				<a href="logout.php">	
					<span class="glyphicon glyphicon-off" aria-hidden="true"></span>&nbsp;
					Logout
				</a>
			</li>
		</ul>

	</div>
    </div>
</nav>

<div class="container">
  <h2>Register Form</h2>
  <p>Register yourself for cool pics!!!</p>
  <form class="form" id="FileUploadForm" action="register.php" method="POST">
      <div class="form-group">
          <h3><label for="email">Please enter a genuine email id as a confirmation code will be send to your email.</label></h3>
      </div>
      <div class="form-group">
          <label for="email">UserName:</label>
          <input type="text" name="txtNameUser" class="form-control" placeholder="Enter user name">
      </div>
      <div class="form-group">
          <label for="email">Email:</label>
          <input type="email" class="form-control" id="email" placeholder="Enter email (valid)" name="txtemail">
      </div>
      <div class="form-group">
          <label for="pwd">PassWord:</label>
          <input type="password" class="form-control" id="pwd" placeholder="Enter password" name="txtpwd">
      </div>
      <center><input type="submit" class="btn btn-default" value="Register" id="RegisterButton" name="RegisterButton">
      </center>
    
</form>
</div>

<?php
        echo "<center><h2> If you are already registered go to <a href='login.php'>Login Page</a> to enter CoolPics</h2></center>";
        $flag4=0;
        if (isset($_SESSION['username']))
        {
               ;
        }
        else { $_SESSION['username']=""; }
 
	if(isset($_REQUEST['RegisterButton'])) {
        if($_SESSION['username']==""){
        $id="";
	if(isset($_REQUEST['txtNameUser']))
	{
		$username = $_REQUEST['txtNameUser'];
	}
	else
	{
		$username = "";
	}
	if(isset($_REQUEST['txtemail']))
	{
		$email = $_REQUEST['txtemail'];
	}
	else
	{
		$email = "";
	}
        if(isset($_REQUEST['txtpwd']))
	{
		$password = $_REQUEST['txtpwd'];
	}
	else
	{
		$password = "";
	}	
		
		if($username=="" || $email=="" || $password=="")
		{
			echo "Error! some of  the required fields are empty!!";
		}
		else
		{
                     $con = mysqli_connect("localhost", "root", "");
	mysqli_select_db($con, "");
                    $sql1 = "Select * from tbluser";
                    $rs1 = mysqli_query($con, $sql1);
		$flag2=0;
		while($row1 = mysqli_fetch_array($rs1))
		{ 
                       if($row1['colUName']==$username){
                           $flag2 = 1;
                       }
                }
                  if($flag2==1)
                  {    echo "Error! username already exists!!"; }
                  else {
                      $confirmcode = rand();
                      $sql = "Insert into tbluser(colUId,colUName,colUEmail,colUPwd,colConfirm,colConfirmCode) values('$id','$username','$email','$password','0','$confirmcode')";
                      $rs = mysqli_query($con, $sql);
                      $message = 
                      "   
                       confirm your email!
                       please click the link below to confirm your account in coolpics.
                       https://iit2016036.000webhostapp.com/emailconfirm.php?username=$username&code=$confirmcode
                      ";
                      mail($email,"CoolPics confirm email", $message, "From: DoNotReply@coolpics.com");
			
					echo "<center><h2>You are Added successfully!!! please confirm your mail. Then login.</h2></center>";
                                        $flag4=1;
                        
                        }
		mysqli_close($con);
	
         }
         }
       else { echo '<br><pre>           <font color="red">    you are already logged in '.$_SESSION['username'].'. Please logout first. </font></pre>'; }
     }
     
?>

</body>
</html>
