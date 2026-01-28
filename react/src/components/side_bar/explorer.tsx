import ArticleOutlinedIcon from '@mui/icons-material/ArticleOutlined';
import FolderIcon from '@mui/icons-material/Folder';
import FolderOpenIcon from '@mui/icons-material/FolderOpen';
import { Box } from "@mui/material";
import { RichTreeView } from '@mui/x-tree-view/RichTreeView';
import { useState } from 'react';
import { useNavigate } from "react-router-dom";

import type { Tree } from '@/src/lib/types';

import RequestHandler from "@/src/lib/request_handler";
import TreeHandler from '@/src/lib/tree_handler';
import loadingState from "@/src/store/loading_store";
import userStore from "@/src/store/user_store";


function Explorer(props: { node_id: string, tree: Tree }) {
  const navigate = useNavigate();
  const { id_token, setTree } = userStore();
  const { setLoading } = loadingState();
  const [expandedItems, setExpandedItems] = useState<string[]>([]);

  const requests = new RequestHandler(id_token);
  const tree_handler = new TreeHandler(props.tree);
  const parents = tree_handler.getParentNodeIds(props.node_id);
  const displayedExpanded = [
    ...new Set([...expandedItems, ...parents]),
  ];

  async function updateLabel(node_id: string, label: string) {
    setLoading(true);

    const res = await requests.put<Tree>(
      `${import.meta.env.VITE_API_HOST}/api/tree/node/label/${node_id}`,
      { label: label }
    );

    setTree(res.body);
    setLoading(false);
  }

  return (
    <>
      <Box >
        <RichTreeView
          sx={{}}
          items={[props.tree]}
          onItemClick={(_, id) => {
            navigate(`/main/${id}`);
          }}
          selectedItems={props.node_id}
          expandedItems={displayedExpanded}
          onExpandedItemsChange={(_, ids) => setExpandedItems(ids)}
          isItemEditable
          onItemLabelChange={(itemId, label) => updateLabel(itemId, label)}
          slots={{
            expandIcon: FolderIcon,
            collapseIcon: FolderOpenIcon,
            endIcon: ArticleOutlinedIcon,
          }}
        />
      </Box>
    </>
  );
};

export default Explorer;