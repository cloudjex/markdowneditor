import { Alert, Button, TextField } from "@mui/material";
import { useEffect, useState } from "react";
import { useForm } from "react-hook-form";
import { useNavigate } from "react-router-dom";

import loadingState from "../store/loading_store";
import userStore from '../store/user_store';
import request_utils from "../utils/request_utils";

import type { SigninForm, SigninResponse, TreeResponse } from "../types/types";

function Signin() {
  const navigate = useNavigate();
  const { setEmail, setIdToken, resetUserState, setNodeTree } = userStore();
  const { setLoading, resetLoadingState } = loadingState();

  const [signinError, setSigninError] = useState<boolean>(false);

  useEffect(() => {
    resetUserState();
    resetLoadingState();
  }, []);

  const {
    register,
    handleSubmit,
    formState: { errors },
  } = useForm<SigninForm>();

  const onSubmit = async (data: SigninForm) => {
    setLoading(true);
    setSigninError(false);

    const signin_res_promise = request_utils.requests<SigninResponse>(
      `${import.meta.env.VITE_API_HOST}/api/signin`,
      "POST",
      {},
      {
        email: data.email,
        password: data.password,
      }
    );
    const signin_res = await signin_res_promise;


    if (signin_res.status != 200) {
      setSigninError(true);
      setLoading(false);
      throw new Error(`signin error`);
    };

    const signin_body = signin_res.body;
    const id_token = signin_body.id_token;
    const email = signin_body.email;

    const res_promise2 = request_utils.requests<TreeResponse>(
      `${import.meta.env.VITE_API_HOST}/api/trees`,
      "GET",
      { authorization: `Bearer ${id_token}` },
      {}
    );
    const res2 = await res_promise2;

    setLoading(false);

    const node_tree = res2.body.node_tree;
    setNodeTree(node_tree);
    setIdToken(id_token);
    setEmail(email);
    navigate(`/main?id=${node_tree.id}`);
  };

  return (
    <>
      <form onSubmit={handleSubmit(onSubmit)}>
        <TextField
          label="メールアドレス"
          fullWidth
          margin="normal"
          {...register("email", {
            required: "メールアドレスは必須です",
          })}
          error={!!errors.email}
          helperText={errors.email?.message}
        />

        <TextField
          label="パスワード"
          type="password"
          fullWidth
          margin="normal"
          {...register("password", {
            required: "パスワードは必須です",
          })}
          error={!!errors.password}
          helperText={errors.password?.message}
        />

        <Button
          type="submit"
          fullWidth
          variant="contained"
          sx={{ mt: 3 }}
        >
          Sign In
        </Button>

        {signinError && (
          <Alert severity="error" sx={{ mt: 2 }}>
            メールアドレスまたはパスワードが正しくありません
          </Alert>
        )}
      </form>
    </>
  );
};

export default Signin;