<?php
if ($_SERVER['REQUEST_METHOD'] === 'POST') {
  $name = htmlspecialchars($_POST['name']);
  $email = filter_var($_POST['email'], FILTER_SANITIZE_EMAIL);
  $phone = htmlspecialchars($_POST['phone']);
  $message = htmlspecialchars($_POST['message']);

  $to = 'your-email@example.com'; // TODO: Replace with your actual email
  $subject = "New Lead from Hairfree Landing Page";
  $body = "Name: $name\nEmail: $email\nPhone: $phone\nMessage: $message";
  $headers = "From: contact@yourdomain.com\r\n" .
             "Reply-To: $email\r\n" .
             "X-Mailer: PHP/" . phpversion();

  if (mail($to, $subject, $body, $headers)) {
    echo "<script>alert('Thank you! We will contact you shortly.'); window.location = 'index.html';</script>";
  } else {
    echo "<script>alert('Sorry, there was a problem submitting your form.'); window.history.back();</script>";
  }
} else {
  echo "<script>alert('Invalid request.'); window.location = 'index.html';</script>";
}
?>
