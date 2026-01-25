import { Backdrop, CircularProgress } from '@mui/material';

import loadingState from '@/src/store/loading_store';


function Loading() {
  const { loading_stack } = loadingState();

  return (
    <Backdrop
      sx={(theme) => ({ color: '#fff', zIndex: theme.zIndex.drawer + 1 })}
      open={loading_stack > 0}
    >
      <CircularProgress color="inherit" />
    </Backdrop>
  );
}

export default Loading;
