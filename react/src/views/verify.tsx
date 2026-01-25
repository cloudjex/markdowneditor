import { Alert, Button, Container, Typography } from "@mui/material";
import { MuiOtpInput } from 'mui-one-time-password-input';
import { useState } from "react";
import { useForm } from "react-hook-form";
import { useNavigate } from "react-router-dom";

import Header from "@/src/components/header/header";
import RequestHandler from "@/src/lib/request_handler";
import loadingState from "@/src/store/loading_store";
import userStore from '@/src/store/user_store';


function Verify() {
  const navigate = useNavigate();
  const { setLoading } = loadingState();
  const { email } = userStore();

  const [otp, setOtp] = useState('');
  const [verifyError, setVerifyError] = useState(false);

  const requests = new RequestHandler();

  const handleChange = (newValue: string) => {
    setOtp(newValue);
  };

  const { handleSubmit } = useForm();

  async function onSubmit() {
    if (otp.length < 6) {
      setVerifyError(true);
      throw new Error("invalid otp");
    }

    setVerifyError(false);
    setLoading(true);

    const normalized_otp = otp.replace(/[０-９]/g, s => String.fromCharCode(s.charCodeAt(0) - 0xFEE0));

    const res_promise = requests.post(
      `${import.meta.env.VITE_API_HOST}/api/signup/verify`,
      { email: email, otp: normalized_otp }
    );
    const res = await res_promise;

    setLoading(false);

    if (res.status != 200) {
      setVerifyError(true);
      throw new Error("signup error");
    };

    navigate("/");
  };

  return (
    <>
      <title>Verify</title>
      <Header />

      <Container
        maxWidth="xs"
        sx={{
          marginTop: 7,
          border: "1px solid #ddd",
          borderRadius: "10px",
          padding: "15px",
        }}
      >
        <Typography
          variant="body1"
          sx={{ mb: 3 }}
        >
          メールアドレスに添付された認証コードを入力し、ユーザ登録を完了してください
        </Typography>

        <form onSubmit={handleSubmit(onSubmit)}>

          <MuiOtpInput
            value={otp}
            onChange={handleChange}
            length={6}
            autoFocus
          />

          <Button
            type="submit"
            fullWidth
            variant="contained"
            sx={{ mt: 5 }}
          >
            送信
          </Button>

          {verifyError && (
            <Alert severity="error" sx={{ mt: 2 }}>
              認証コードが正しくありません
            </Alert>
          )}

        </form>
      </Container >
    </>
  );
};

export default Verify;