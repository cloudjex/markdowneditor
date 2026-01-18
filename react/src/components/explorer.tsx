import ArticleOutlinedIcon from '@mui/icons-material/ArticleOutlined';
import FolderIcon from '@mui/icons-material/Folder';
import FolderOpenIcon from '@mui/icons-material/FolderOpen';
import { Box, Typography } from "@mui/material";
import { RichTreeView } from '@mui/x-tree-view/RichTreeView';
import { useState } from 'react';
import { useNavigate, useLocation } from "react-router-dom";

import userStore from "../store/user_store";
import tree_utils from "../utils/tree_utils";

import TreeUpdate from './tree_update';

function Explorer() {
  const navigate = useNavigate();
  const location = useLocation();

  const { id_token, node_tree } = userStore();
  const [expandedItems, setExpandedItems] = useState<string[]>(["/Nodes"]);

  const searchParams = new URLSearchParams(location.search);
  const url_node_id = searchParams.get('id') || "/Nodes";

  const parents = tree_utils.get_parent_node_ids(node_tree, url_node_id);
  let displayedExpanded: string[];
  if (parents){
    displayedExpanded = [...new Set([...expandedItems, ...parents])];
  } else {
    displayedExpanded = [...new Set([...expandedItems])];
  }


  const handleItemClick = (_: React.MouseEvent<Element, MouseEvent>, itemId: string) => {
    navigate(`/main?id=${itemId}`);
  };

  if (id_token && node_tree) {
    return (
      <>
        <Typography variant="h5" sx={{ mt: 2 }}>
          Explorer
        </Typography>

        <TreeUpdate currentNodeId={url_node_id} />

        <Box >
          <RichTreeView
            sx={{ backgroundColor: "rgba(245, 245, 245)" }}
            items={[node_tree]}
            onItemClick={handleItemClick}
            selectedItems={url_node_id}
            expandedItems={displayedExpanded}
            onExpandedItemsChange={(_, ids) => setExpandedItems(ids)}
            slots={{
              expandIcon: FolderIcon,
              collapseIcon: FolderOpenIcon,
              endIcon: ArticleOutlinedIcon,
            }}
          />
        </Box>
      </>
    );
  }
};

export default Explorer;