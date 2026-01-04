import { Alert, Button, Container, TextField } from "@mui/material";
import { useState } from "react";
import { useForm } from "react-hook-form";
import { useNavigate } from "react-router-dom";

import Header from "../components/header";
import loadingState from "../store/loading_store";
import userStore from "../store/user_store";
import request_utils from "../utils/request_utils";

import type { Otp } from "../types/types";

function Verify() {
  const navigate = useNavigate();
  const { email } = userStore();
  const { setLoading } = loadingState();
  const [otpError, setOtpError] = useState(false);

  const {
    register,
    handleSubmit,
    formState: { errors },
  } = useForm<Otp>();

  const onSubmit = async (data: Otp) => {
    setLoading(true);

    const res_promise = request_utils.requests(
      `${import.meta.env.VITE_API_HOST}/api/signup/verify`,
      "POST",
      {},
      {
        otp: data.otp,
        email: email
      }
    );
    const res = await res_promise;

    setLoading(false);

    if (res.status != 200) {
      setOtpError(true);
      throw new Error(`invalid otp`);
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
          marginTop: 3,
          border: "1px solid #ddd",
          borderRadius: "10px",
          padding: "15px",
        }}
      >

        <form onSubmit={handleSubmit(onSubmit)}>
          <TextField
            label="ワンタイムパスワード"
            fullWidth
            margin="normal"
            {...register("otp", {
              required: "ワンタイムパスワードは必須です",
            })}
            error={!!errors.otp}
            helperText={errors.otp?.message}
          />

          <Button
            type="submit"
            fullWidth
            variant="contained"
            sx={{ marginTop: "5%" }}
          >
            Sign Up
          </Button>

          {otpError && (
            <Alert severity="error" sx={{ mt: 2 }}>
              ワンタイムパスワードが正しくありません
            </Alert>
          )}

        </form>

      </Container>
    </>
  );
};

export default Verify;