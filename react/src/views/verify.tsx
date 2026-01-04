import { Alert, Button, Container, Typography } from "@mui/material";
import { MuiOtpInput } from 'mui-one-time-password-input';
import { useState } from "react";
import { useForm } from "react-hook-form";
import { useNavigate } from "react-router-dom";

import Header from "../components/header";
import loadingState from "../store/loading_store";
import userStore from '../store/user_store';
import request_utils from "../utils/request_utils";

function Verify() {
  const navigate = useNavigate();
  const { setLoading } = loadingState();
  const { email } = userStore();

  const [otp, setOtp] = useState<string>('');
  const [verifyError, setVerifyError] = useState<boolean>(false);

  const handleChange = (newValue: string) => {
    setOtp(newValue);
  };

  const {
    handleSubmit,
  } = useForm();

  const onSubmit = async () => {
    if (otp.length < 6) {
      setVerifyError(true);
      throw new Error(`invalid otp`);
    }

    setVerifyError(false);
    setLoading(true);

    const res_promise = request_utils.requests(
      `${import.meta.env.VITE_API_HOST}/api/signup/verify`,
      "POST",
      {},
      {
        email: email,
        otp: otp,
      }
    );
    const res = await res_promise;

    setLoading(false);

    if (res.status != 200) {
      setVerifyError(true);
      throw new Error(`signup error`);
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
          sx={{ marginBottom: 5 }}
        >
          メールアドレスに添付されたワンタイムパスワードを入力し、ユーザ登録を完了してください
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
            sx={{ marginTop: "5%" }}
          >
            Sign Up
          </Button>

          {verifyError && (
            <Alert severity="error" sx={{ mt: 2 }}>
              ワンタイムパスワードが正しくありません
            </Alert>
          )}

        </form>
      </Container >
    </>
  );
};

export default Verify;